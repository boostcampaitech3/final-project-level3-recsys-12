import os
from box import Box
import torch.optim as optim

from utils import random_seed, sparse2Tensor
from dataset import AEDataset
from trainer import Trainer
from model import VAE

import torch
import pandas as pd
import numpy as np

##############################ARGS##################################
args = {
    ######data#######
    'min_user_cnt' : 100,
    'min_item_cnt' : 50,
    'n_heldout' : 1000,
    'target_prop' : 0.2,
    'min_item_to_split' : 5,
    
    #####model######
    'hidden_dim' : 600, # 600
    'latent_dim' : 200, # 200
    'stnd_mixture_weight' : 3/20,
    'post_mixture_weight' : 3/4,
    'unif_mixture_weight' : 1/10,
    'dropout_ratio' : 0.3,
    
    #####optimizer####
    'lr' : 1e-4,
    'wd' : 0.00,
    
    ######trainer#####
    'batch_size' : 256, #256
    'epochs' : 100, #100
    'en_epochs' : 3, #3
    'de_epochs' : 1, #1
    'beta' : None,
    'gamma' : 0.005, #0.005
    'not_alter' : False,
    'ndcg_k' : 10,
    'recall_k' : 10,
    'verbose' : True,
    
    #####etc#######
    'base_dir' : '../../data/',
    'random_seed' : 42,
    'device' : 'cuda'
}
args = Box(args)
##############################ARGS##################################

##############################PATHS##################################
dir_output = os.path.join(os.getcwd(), 'output')
##############################PATHS##################################
    
random_seed(args.random_seed)


data_kwargs = {
    'base_dir' : args.base_dir,
    'seed' : args.random_seed,

    'min_user_cnt' : args.min_user_cnt,
    'min_item_cnt' : args.min_item_cnt,

    'n_heldout' : args.n_heldout,
    'target_prop' : args.target_prop,
    'min_item_to_split' : args.min_item_to_split
}


data = AEDataset(**data_kwargs)

datasets = data.datasets # dict, {train_data, valid_data(input, target), test_data(input, target), inference_data}
input_dim = data.n_items

model_kwargs = {
    'hidden_dim' : args.hidden_dim,
    'latent_dim' : args.latent_dim,
    'input_dim' : input_dim,

    'mixture_weights' : [args.stnd_mixture_weight,
                         args.post_mixture_weight,
                         args.unif_mixture_weight],
}

model = VAE(**model_kwargs).to(args.device)
model_best = VAE(**model_kwargs).to(args.device)

decoder_param = set(model.decoder.parameters())
encoder_param = set(model.encoder.parameters())

optimizer_encoder = optim.Adam(encoder_param, lr=args.lr, weight_decay=args.wd)
optimizer_decoder = optim.Adam(decoder_param, lr=args.lr, weight_decay=args.wd)

trainer_kwargs = {
    #model & optimizer
    'model' : model,
    'model_best' : model_best,
    'optimizer_encoder' : optimizer_encoder,
    'optimizer_decoder' : optimizer_decoder,

    #hyperparameters
    'batch_size' : args.batch_size,
    'epochs' : args.epochs,
    'en_epochs' : args.en_epochs,
    'de_epochs' : args.de_epochs,
    'beta' : args.beta,
    'gamma' : args.gamma,
    'dropout_ratio' : args.dropout_ratio,
    'not_alter' : args.not_alter,
    'ndcg_k' : args.ndcg_k,
    'recall_k' : args.recall_k,

    #datasets 
    'datasets' : datasets, 

    #etc
    'output_path' : dir_output,
    'model_name' : 'RecVAE',
    'device' : args.device,
    'verbose' : args.verbose,

    # label encoder
    'user_encoder' : data.user_encoder,
    'item_encoder' : data.item_encoder
}

trainer = Trainer(**trainer_kwargs)

trainer.run()
trainer.test()

def inference(trainer, data, k):
    
    best_model = trainer.model_best
    input_data = sparse2Tensor(trainer.inference_data).to(trainer.device)
    users = range(data.n_users)
    model.eval()
    
    with torch.no_grad():
        prediction = model(input_data, calculate_loss=False)
        print(prediction.size())
        prediction[torch.nonzero(input_data, as_tuple=True)] = -np.inf
        scores, movies = torch.topk(prediction, dim=1, k=k)
        
        users = np.tile(users, (k,1)).T
        user_list = np.concatenate([user for user in users])
        score_list = torch.cat([score for score in scores])
        movie_list = torch.cat([movie for movie in movies])
    
    user_decoder = {value : key for (key, value) in trainer.user_encoder.items()}
    item_decoder = {value : key for (key, value) in trainer.item_encoder.items()}
    
    inference_df = pd.DataFrame()
    inference_df['user'] = user_list
    inference_df['item'] = movie_list.cpu().numpy()
    inference_df['score'] = score_list.cpu().numpy()
    
    inference_df['user'] = inference_df['user'].apply(lambda x : user_decoder[x])
    inference_df['item'] = inference_df['item'].apply(lambda x : item_decoder[x])

    return inference_df

inference_df = inference(trainer, data, k=10)
inference_df = inference_df.sort_values(['user', 'score'], ascending=[True, False])

if not os.path.exists('result/'):
            os.mkdir('result')
            
inference_df.to_csv('result/output.csv', index=False)