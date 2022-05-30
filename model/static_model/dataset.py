from logging.config import valid_ident
import pandas as pd
import numpy as np
from copy import deepcopy
from scipy import sparse

def fix_seed(num:int)-> None:
    np.random.seed(num)

def preprocessing(data:pd.DataFrame) -> pd.DataFrame:
    data.rename(columns={"User-ID" : "user", "ISBN" : "item", "Book-Rating" : 'rating'}, inplace=True)
    data['rating'] = data['rating'].replace(0.0, 5.0)
    return data
    
def filtering_data(data:pd.DataFrame, cnt:int, by:str='user') -> pd.DataFrame:
    
    if by == 'user' : A, B = 'user', 'item'
    elif by == 'item' : A, B = 'item', 'user'
            
    count_B_by_A = data.groupby(A).agg({B :'count'})
    valid_ = list(count_B_by_A[count_B_by_A[B] >= cnt].index)
    valid_data = data[data[A].isin(valid_)]
    
    return valid_data

class AEDataset():
    def __init__(self, seed, min_user_cnt, min_item_cnt, n_heldout, target_prop, min_item_to_split):
        
        # fix_seed
        fix_seed(seed)
        
        # load data
        self.raw_data = pd.read_csv('data/Ratings.csv', header=0)
        self.data = preprocessing(self.raw_data)
        
        # filtering data
        self.data = filtering_data(self.data, min_user_cnt, by='user')
        self.data = filtering_data(self.data, min_item_cnt, by='item')
        
        # unique user and item
        self.users = np.unique(self.data['user'])
        self.n_users = len(self.users)
        self.items = np.unique(self.data['item'])
        self.n_items = len(self.items)
        
        # train, valid, test split
        self.n_heldout = n_heldout
        self.train_users, self.valid_users, self.test_users = self._user_split()
        self.train_data, self.valid_data, self.test_data = self._get_data()
        
        # input_target split
        self.target_prop = target_prop
        self.min_item_to_split = min_item_to_split
        self.train_input = deepcopy(self.train_data)
        self.valid_input, self.valid_target = self._input_target_split(self.valid_data)
        self.test_input, self.test_target = self._input_target_split(self.test_data)
        
        # label encode
        for data in [self.train_input, self.valid_input, self.valid_target, self.test_input, self.test_target]:
            self.user_encoder, self.item_encoder = self._label_encode(data)
        
        # raw data to sparse matrix
        self.train_matrix = self._data_to_matrix('train')
        self.valid_matrix_input, self.valid_matrix_target = self._data_to_matrix('valid')
        self.test_matrix_input, self.test_matrix_target = self._data_to_matrix('test')

        # inference data
        self.inference_matrix = self._make_inference_dataset()
        
        self.datasets = {'train_data' : self.train_matrix,
                         'valid_data' : (self.valid_matrix_input, self.valid_matrix_target),
                         'test_data' : (self.test_matrix_input, self.test_matrix_target),
                         'inference_data' : self.inference_matrix}
        
        
    def _user_split(self):
        
        print('user split...')
        i_shuffle = np.random.permutation(self.n_users)
        self.users = self.users[i_shuffle]
        
        train_users = self.users[:(self.n_users - self.n_heldout*2)]
        valid_users = self.users[(self.n_users - self.n_heldout*2) : (self.n_users - self.n_heldout)]
        test_users = self.users[(self.n_users - self.n_heldout) : ]
    
        return train_users, valid_users, test_users
    
    def _get_data(self):
        
        print('getting data...')
        train_data = self.data.loc[self.data['user'].isin(self.train_users)]
        self.train_items = pd.unique(train_data['item'])
        
        valid_data = self.data.loc[self.data['user'].isin(self.valid_users)]
        valid_data = valid_data.loc[valid_data['item'].isin(self.train_items)]
        
        test_data = self.data.loc[self.data['user'].isin(self.test_users)]
        test_data = test_data.loc[test_data['item'].isin(self.train_items)]
        
        return train_data, valid_data, test_data
    
    def _input_target_split(self, data):
        
        print(f'input target split...')
        data_grby_user = data.groupby('user')
        input_list, target_list = list(), list()
        
        for _, group in data_grby_user :
            
            n_items_of_user = len(group)
            
            if n_items_of_user >= self.min_item_to_split :
                
                index = np.zeros(n_items_of_user, dtype='bool')
                index[np.random.choice(n_items_of_user, size=int(self.target_prop * n_items_of_user), replace=False).astype('int64')] = True
                
                input_list.append(group[np.logical_not(index)])
                target_list.append(group[index])
                
            else :
                input_list.append(group)
                
        input = pd.concat(input_list)
        target = pd.concat(target_list)
        
        return input, target
    
    def _label_encode(self, data) :
        
        print('encoding...')
        
        user2id = dict((user, i) for (i, user) in enumerate(self.users))
        item2id = dict((item, i) for (i, item) in enumerate(self.train_items))
        
        user_id = data['user'].apply(lambda x : user2id[x])
        item_id = data['item'].apply(lambda x : item2id[x])
        data['user'] = user_id
        data['item'] = item_id
        
        return user2id, item2id
    
    def _data_to_matrix(self, data_type) :
        
        if data_type == 'train':
            
            n_users = self.train_input['user'].max() + 1
            rows, cols = self.train_input['user'], self.train_input['item']
            matrix = sparse.csr_matrix((np.ones_like(rows), (rows, cols)), 
                                     dtype='float64',
                                     shape=(n_users, self.n_items))
            return matrix
        
        if data_type == 'valid':
            input = self.valid_input
            target = self.valid_target
        
        if data_type == 'test' :
            input = self.test_input
            target = self.test_target

        start_idx = min(input['user'].min(), target['user'].min())
        end_idx = max(input['user'].max(), target['user'].max())

        rows_input, cols_input = input['user'] - start_idx, input['item']
        rows_target, cols_target = target['user'] - start_idx, target['item']
        
        matrix_input = sparse.csr_matrix((np.ones_like(rows_input), (rows_input, cols_input)), 
                                         dtype='float64',
                                         shape=(end_idx - start_idx + 1, self.n_items))
        
        matrix_target = sparse.csr_matrix((np.ones_like(rows_target),
                                       (rows_target, cols_target)), dtype='float64',
                                       shape=(end_idx - start_idx + 1, self.n_items))
        
        return matrix_input, matrix_target
    
    def _make_inference_dataset(self) :
        
        data = self.data.loc[self.data['item'].isin(self.train_items)]
        self.user_encoder, self.item_encoder = self._label_encode(data)
        
        n_users = self.n_users
        n_items = len(data['item'].unique())
        rows, cols = data['user'], data['item']    
        matrix = sparse.csr_matrix((np.ones_like(rows), (rows, cols)), 
                                 dtype='float64',
                                 shape=(n_users, n_items))
        
        sparse.save_npz('data/infrence_data.npz', matrix)
        
        self.inference_data = data
        return matrix