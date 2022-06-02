from copyreg import pickle
from math import inf
import os
import torch.optim as optim

from utils import sparse2Tensor
import scipy.sparse as sparse

import torch
import pandas as pd
import numpy as np
import pickle

device = 'cuda'
model_list = os.listdir('output')
model_path = f'output/{model_list[-1]}'

data_path = '../../data/ver2/infrence_data.npz'
with open('infer/user_encoder.pkl', 'rb') as f:
    user_encoder = pickle.load(f)
with open('infer/item_encoder.pkl', 'rb') as f:
    item_encoder = pickle.load(f)

def label_encode(self, data) :
    
    print('encoding...')
    
    user2id = dict((user, i) for (i, user) in enumerate(self.users))
    item2id = dict((item, i) for (i, item) in enumerate(self.train_items))
    
    user_id = data['user'].apply(lambda x : user2id[x])
    item_id = data['item'].apply(lambda x : item2id[x])
    data['user'] = user_id
    data['item'] = item_id
    
    return user2id, item2id


def full_inference(k):
    
    model = torch.load(model_path)
    sparse_data = sparse.load_npz(data_path)
    inference_df = pd.DataFrame(columns={'user', 'item', 'score'})
    
    for start_idx in range(0,sparse_data.shape[0], 30000): 
        end_idx = start_idx + 30000
        input_data = sparse2Tensor(sparse_data[start_idx:end_idx]).to(device)
        users = range(start_idx, end_idx)
        model.eval()
        
        with torch.no_grad():
            prediction = model(input_data, calculate_loss=False)
            prediction[torch.nonzero(input_data, as_tuple=True)] = -np.inf
            scores, movies = torch.topk(prediction, dim=1, k=k)
            
            users = np.tile(users, (k,1)).T
            user_list = np.concatenate([user for user in users])
            score_list = torch.cat([score for score in scores])
            movie_list = torch.cat([movie for movie in movies])

        user_decoder = {value : key for (key, value) in user_encoder.items()}
        item_decoder = {value : key for (key, value) in item_encoder.items()}
        
        temp_df = pd.DataFrame()
        temp_df['user'] = user_list
        temp_df['item'] = movie_list.cpu().numpy()
        temp_df['score'] = score_list.cpu().numpy()
        
        temp_df['user'] = temp_df['user'].apply(lambda x : user_decoder[x])
        temp_df['item'] = temp_df['item'].apply(lambda x : item_decoder[x])

        inference_df = pd.concat(inference_df, temp_df)

    return inference_df

inference_df = full_inference(k=10)
inference_df = inference_df.sort_values(['user', 'score'], ascending=[True, False])

if not os.path.exists('result/'):
            os.mkdir('result')
            
inference_df.to_csv('result/full_inference_output.csv', index=False)
