import numpy as np
import pandas as pd
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from sklearn.preprocessing import LabelEncoder

import torch

book = pd.read_csv('../data/ver2/Book.tsv', sep='\t')
book_genres = pd.read_csv('../data/ver2/Book_Genre.tsv', sep='\t')
ratings = pd.read_csv('../data/ver2/Rating.tsv', sep='\t')

book_genres['ck'] = 1.0

tfidf = TfidfVectorizer(analyzer='word', stop_words='english')
synop_matrix = tfidf.fit_transform(book['synopsis'].values.astype('U'))

cosine_similarities = cosine_similarity(synop_matrix) 

user_encoder = LabelEncoder()
item_encoder = LabelEncoder()
ratings['item'] = item_encoder.fit_transform(ratings['item'])
ratings['user'] = user_encoder.fit_transform(ratings['user'])

rows, cols, data = ratings['user'], ratings['item'], ratings['rating']
n_users = ratings['user'].nunique()
n_items = ratings['item'].nunique()

rating_matrix = sparse.csr_matrix((data, (rows, cols)),
                            dtype='float64',
                            shape=(n_users, n_items))

k = 10

for st_idx in range(0, n_users, 10000):

    next_idx = st_idx + 10000
    end_idx = min(next_idx, n_users)
    input_data = rating_matrix[st_idx:end_idx]
    users = range(st_idx, end_idx)
    
    result = torch.tensor(input_data @ cosine_similarities)
    result[torch.nonzero(torch.FloatTensor(input_data.todense()), as_tuple=True)] = -np.inf
    
    scores, items = torch.topk(result, k=k, dim=1)


    users = np.tile(users, (k,1)).T
    user_list = np.concatenate([user for user in users])
    score_list = torch.cat([score for score in scores])
    item_list = torch.cat([item for item in items])

    temp_df = pd.DataFrame()
    temp_df['user'] = user_list
    temp_df['item'] = item_list.cpu().numpy()
    temp_df['score'] = score_list.cpu().numpy()

    temp_df['user'] = user_encoder.inverse_transform(temp_df['user'])
    temp_df['item'] = user_encoder.inverse_transform(temp_df['item'])

    if st_idx == 0 : inference_df = temp_df
    else : inference_df = pd.concat([inference_df, temp_df])

inference_df = inference_df.sort_values(['user', 'score'], ascending=[True, False])

if not os.path.exists('result/'):
            os.mkdir('result')
            
inference_df.to_csv('result/content_output.csv', index=False)


