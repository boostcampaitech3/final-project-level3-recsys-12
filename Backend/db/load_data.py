import os, gc, json, time
import pandas as pd
from database import engine
from crud import pwd_context

from typing import Tuple, List


def load_json_data(file_path: str):
    gc.collect()
    with open(file_path, 'r') as json_file :
        for line in json_file :
            data = json.loads(line)
            yield data


def get_datas(file_path) -> dict:
    print('\tread json file and parse...')
    start_time = time.time()
    generate_json = load_json_data(file_path)

    user_id = []
    user_name = []
    rating = []
    isbn = []
    review_summary = []

    for data in generate_json:
        user_id.append(data['reviewerID']+'@gmail.com')
        if 'reviewerName' in data: user_name.append(data['reviewerName'])
        else: user_name.append('')
        rating.append(data['overall'])
        isbn.append(data['asin'])
        if 'summary' in data: review_summary.append(data['summary'])
        else: review_summary.append('')
        
    take_time = time.time() - start_time
    print(f'\tread json file and parse done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return {
        'user_id': user_id,
        'user_name': user_name,
        'rating': rating,
        'isbn': isbn,
        'review_summary': review_summary,
    }



def make_users_df(ids: list, names: list) -> pd.DataFrame:
    users_df = pd.DataFrame()
    users_df['id'] = ids
    users_df['name'] = names
    users_df.drop_duplicates(['id'], keep='first', ignore_index=True, inplace=True)
    print('\t\tmake hashed_password...')
    start_time = time.time()
    users_df['hashed_password'] = users_df.apply(
            lambda row:  pwd_context.hash('test'+row.id),
            axis=1
        )
    take_time = time.time() - start_time
    print(f'\t\tmake hashed_password done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return users_df


def make_ratings_df(users: List[str], items: List[str], ratings: List[str], reviews: List[str]) -> pd.DataFrame:
    ratings_df = pd.DataFrame()
    ratings_df['user'] = users
    ratings_df['item'] = items
    ratings_df['rating'] = ratings
    ratings_df['rating'] = ratings_df['rating'].astype('int8')
    ratings_df['reivew'] = reviews

    return ratings_df


def preprocessing_rating_json(file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    print('preprocessing ratings json...: make users and ratings df')
    start_time = time.time()
    datas_dict = get_datas(file_path)
    print('\tmake users df...')
    users_df = make_users_df(ids=datas_dict['user_id'], names=datas_dict['user_name'])
    print('\tusers df done!')
    print('\tmake ratings df...')
    ratings_df = make_ratings_df(
        users=datas_dict['user_id'],
        items=datas_dict['isbn'],
        ratings=datas_dict['rating'],
        reviews=datas_dict['reivew'] ,   
    )
    print('\tratings df done!')
    take_time = time.time() - start_time
    print(f'preprocessing ratings json done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return users_df, ratings_df


def insert_datas(df: pd.DataFrame, engine, table_name: str) -> None:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )



if __name__ == '__main__':
    # excute: nohup /opt/conda/envs/web/bin/python -u /opt/ml/final-project-level3-recsys-12/Backend/db/load_data.py > /opt/ml/insert.log &
    base_dir = os.path.dirname(__file__)
    users_df, ratings_df = preprocessing_rating_json(os.path.join(base_dir, 'datas', 'Books.json'))

    # df_datas = [user_info, book_info, ratings]
    # table_names = ['user_info', 'book_info', 'ratings']

    df_datas = [users_df]
    table_names = ['users']

    for df, table_name in zip(df_datas, table_names):
        print(f'load {table_name}...')
        insert_datas(df=df, engine=engine, table_name=table_name)
        print('Done!')