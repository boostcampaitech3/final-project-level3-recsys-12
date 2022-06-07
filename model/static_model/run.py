import os
from box import Box
import torch.optim as optim

from utils import random_seed, sparse2Tensor
from dataset import TrainDataset
from trainer import Trainer
from model import VAE

import torch
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
##############################ARGS##################################
args = {
    ######data#######
    'min_user_cnt' : 5,
    'min_item_cnt' : 0,
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
    'lr' : 3e-4,
    'wd' : 0.00,
    
    ######trainer#####
    'batch_size' : 256, #256
    'epochs' : 100, #100
    'en_epochs' : 3, #3
    'de_epochs' : 1, #1
    'beta' : None,
    'gamma' : 0.005, #0.005
    'early_stop': 3,

    'not_alter' : False,
    'ndcg_k' : 10,
    'recall_k' : 10,
    'verbose' : True,
    
    #####etc#######
    'base_dir' : '../../data/ver2/',
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


data = TrainDataset(**data_kwargs)

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
    'early_stop' : args.early_stop,
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
    
    model = trainer.model_best
    model.eval()
    # inference_df = pd.DataFrame(columns={'user', 'item', 'score'})

    for start_idx in range(0, trainer.inference_data.shape[0], 10000):
        
        next_idx = start_idx + 10000
        end_idx = min(next_idx, trainer.inference_data.shape[0])
        
        input_data = sparse2Tensor(trainer.inference_data[start_idx:end_idx]).to(trainer.device)
        
        users = range(start_idx, end_idx)

        with torch.no_grad():
            prediction = model(input_data, calculate_loss=False)
            print(prediction.size())
            prediction[torch.nonzero(input_data, as_tuple=True)] = -np.inf
            scores, books = torch.topk(prediction, dim=1, k=k)
            
            users = np.tile(users, (k,1)).T
            user_list = np.concatenate([user for user in users])
            score_list = torch.cat([score for score in scores])
            book_list = torch.cat([book for book in books])
        
        user_decoder = {value : key for (key, value) in trainer.user_encoder.items()}
        item_decoder = {value : key for (key, value) in trainer.item_encoder.items()}
        
        temp_df = pd.DataFrame()
        temp_df['user'] = user_list
        temp_df['item'] = book_list.cpu().numpy()
        temp_df['score'] = score_list.cpu().numpy()
        
        temp_df['user'] = temp_df['user'].apply(lambda x : user_decoder[x])
        temp_df['item'] = temp_df['item'].apply(lambda x : item_decoder[x])
        
        if start_idx == 0 : inference_df = temp_df
        else : inference_df = pd.concat([inference_df, temp_df])

    return inference_df

inference_df = inference(trainer, data, k=10)
# scaler = MinMaxScaler(feature_range=(0,5))
# inference_df['score'] = scaler.fit_transform(inference_df['score'])
inference_df = inference_df.sort_values(['user', 'score'], ascending=[True, False])

if not os.path.exists('../result/'):
            os.mkdir('../result')
            
#inference_df.to_csv('../result/output.csv', index=False)