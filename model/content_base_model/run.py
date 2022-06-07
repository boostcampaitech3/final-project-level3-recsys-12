import numpy as np
import pandas as pd
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from tqdm import tqdm

import torch

def cosine_similarity_n_space(m1, m2, batch_size=500):
    assert m1.shape[1] == m2.shape[1]
    ret = np.ndarray((m1.shape[0], m2.shape[0]))
    for row_i in tqdm(range(0, int(m1.shape[0] / batch_size) + 1)):
        start = row_i * batch_size
        end = min([(row_i + 1) * batch_size, m1.shape[0]])
        if end <= start:
            break 
        rows = m1[start: end]
        sim = cosine_similarity(rows, m2)
        ret[start: end] = sim
    return ret


def similarity_cosine_by_index(indicies):
    return cosine_similarity(X=synop_matrix[indicies], Y=synop_matrix)

book = pd.read_csv('../../data/ver2/Book.tsv', sep='\t')
ratings = pd.read_csv('../../data/ver2/Rating.tsv', sep='\t', low_memory=False)

tfidf = TfidfVectorizer(analyzer='word', stop_words='english')
synop_matrix = tfidf.fit_transform(book['synopsis'].values.astype('U'))
synop_matrix = synop_matrix.astype('float32')

# chunk_size = 10000
# matrix_len = synop_matrix.shape[0]

cosine_similarities = cosine_similarity(synop_matrix)

user_encoder = LabelEncoder()
item_encoder = LabelEncoder()


ratings['item'] = item_encoder.fit_transform(ratings['item'])
ratings['user'] = user_encoder.fit_transform(ratings['user'])

user_cnt = ratings.groupby('user').agg({'item' : 'count'})
valid_users = list(user_cnt[user_cnt['item'] < 10].index)

rows, cols, data = ratings['user'], ratings['item'], ratings['rating']
n_users = ratings['user'].nunique()
n_items = ratings['item'].nunique()

rating_matrix = sparse.csr_matrix((data, (rows, cols)),
                            dtype='float32',
                            shape=(n_users, n_items))

# for valid_user in valid_users :
#     user_ratings = ratings[ratings['user'] == valid_user]
#     cosine_similarities = similarity_cosine_by_index(user_ratings['item'])
#     result = torch.tensor(user_ratings @ cosine_similarities)
#     print(result.shape)

k = 10
#for chunk_start in tqdm(range(0, matrix_len, chunk_size)):
    

for st_idx in tqdm(range(0, n_users, 10000)):

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
    temp_df['item'] = item_encoder.inverse_transform(temp_df['item'])

    if st_idx == 0 : inference_df = temp_df
    else : inference_df = pd.concat([inference_df, temp_df])

inference_df = inference_df.sort_values(['user', 'score'], ascending=[True, False])

scaler = MinMaxScaler(feature_range=(0,5))
# inference_df['score'] = scaler.fit_transform(inference_df['score'])

if not os.path.exists('../result/'):
            os.mkdir('../result')
            
inference_df.to_csv('../result/content_output.csv', index=False)


