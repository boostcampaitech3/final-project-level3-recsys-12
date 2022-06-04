import os, sys,  gc, json, time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from db.database import engine
from db.crud import pwd_context

from typing import Tuple, List


def load_json_data(file_path: str):
    gc.collect()
    with open(file_path, 'r') as json_file :
        for line in json_file :
            data = json.loads(line)
            yield data


def get_rating_datas(file_path) -> dict:
    print('\tread json file and parse...')
    start_time = time.time()
    generate_json = load_json_data(file_path)

    user_id = []
    user_name = []
    rating = []
    isbn = []

    for data in generate_json:
        if data['asin'][0] == 'B': continue
        user_id.append(data['reviewerID']+'@gmail.com')
        if 'reviewerName' in data: user_name.append(data['reviewerName'])
        else: user_name.append('')
        rating.append(data['overall'])
        isbn.append(data['asin'])

    take_time = time.time() - start_time
    print(f'\tread json file and parse done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return {
        'user_id': user_id,
        'user_name': user_name,
        'rating': rating,
        'isbn': isbn,
    }



def make_users_df(ids: list, names: list) -> pd.DataFrame:
    users_df = pd.DataFrame()
    users_df['id'] = ids
    users_df['name'] = names
    users_df.drop_duplicates(['id'], keep='first', ignore_index=True, inplace=True)
    print('\t\tmake hashed_password...')
    start_time = time.time()
    hashed_password = pwd_context.hash('test')
    users_df['hashed_password'] = hashed_password
    take_time = time.time() - start_time
    print(f'\t\tmake hashed_password done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return users_df


def make_ratings_df(users: List[str], items: List[str], ratings: List[str]) -> pd.DataFrame:
    ratings_df = pd.DataFrame()
    ratings_df['user'] = users
    ratings_df['item'] = items
    ratings_df['rating'] = ratings
    ratings_df['rating'] = ratings_df['rating'].astype('int8')

    # 한 유저가 같은 아이템에 대해 여러 rating을 줘서 일단 제일 높은 것을 고른다.
    # 향후엔 제일 최근 rating을 가져오는 게 좋을 것 같다.
    ratings_df.sort_values(['rating'], ascending=False, inplace=True)
    ratings_df.drop_duplicates(subset=['item', 'user'], keep='first', inplace=True)
    ratings_df.reset_index(drop=True)

    return ratings_df


def preprocessing_rating_json(file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    print('preprocessing ratings json...: make users and ratings df')
    start_time = time.time()
    datas_dict = get_rating_datas(file_path)
    print('\tmake users df...')
    users_df = make_users_df(ids=datas_dict['user_id'], names=datas_dict['user_name'])
    print('\tusers df done!')
    print('\tmake ratings df...')
    ratings_df = make_ratings_df(
        users=datas_dict['user_id'],
        items=datas_dict['isbn'],
        ratings=datas_dict['rating'], 
    )
    print('\tratings df done!')
    take_time = time.time() - start_time
    print(f'preprocessing ratings json done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return users_df, ratings_df


def make_df_of_meta(gen_meta, img_etc_df) -> pd.DataFrame:
    isbns, titles = list(), list()

    for data in gen_meta:
        if data['asin'][0] == 'B': continue
        isbns.append(data['asin'])
        titles.append(data['title'])


    books = pd.DataFrame()
    books['id'] = isbns
    books['title'] = titles

    book_merge = pd.merge(books, img_etc_df, left_on='id', right_on='id', how='left')

    return book_merge


def get_meta_datas_df(file_path: str, img_etc_path: str) -> pd.DataFrame:
    gen_meta_json = load_json_data(file_path)
    img_etc_df = pd.read_csv(img_etc_path, sep='\t')
    img_etc_df.drop(labels='title', axis=1, inplace=True)
    img_etc_df['publication_year'] = img_etc_df.apply(
                                lambda row: 0 if row['publication_year']=='None' else row['publication_year'][:4],
                                axis=1
                            )

    books = make_df_of_meta(gen_meta_json, img_etc_df)
    return books


def preprocessing_book_meta_json(file_path: str, img_etc_path: str) -> pd.DataFrame:
    print('preprocessing book meta json...: make book df')
    start_time = time.time()
    book_df = get_meta_datas_df(file_path, img_etc_path)
    
    take_time = time.time() - start_time
    print(f'preprocessing book meta json done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')
    return book_df


def preprocessing_book_genre(
    genre_path: str,
    book_genre_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:

    print('preprocessing genre tsv ...: make genre, book_genre df')
    start_time = time.time()

    genre_df = pd.read_csv(genre_path, sep='\t')
    book_genre_df = pd.read_csv(book_genre_path, sep='\t')

    take_time = time.time() - start_time
    print(f'preprocessing genre tsv done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return genre_df, book_genre_df

def preprocessing_book_author(
    author_path: str,
    book_autor_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:

    print('preprocessing author tsv ...: make author, book_author df')
    start_time = time.time()

    author_df = pd.read_csv(author_path, sep='\t')
    book_autor_df = pd.read_csv(book_autor_path, sep='\t')

    take_time = time.time() - start_time
    print(f'preprocessing author tsv done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return author_df, book_autor_df

def preprocessing_inference(
    inference_path: str)-> Tuple[pd.DataFrame, pd.DataFrame]:

    print('preprocessing inference csv ...: make author, book_author df')
    start_time = time.time()

    inference_df = pd.read_csv(inference_path)

    take_time = time.time() - start_time
    print(f'preprocessing inference csv done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return inference_df


def insert_datas(df: pd.DataFrame, engine, table_name: str) -> None:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )


if __name__ == '__main__':
    # excute: nohup /opt/conda/envs/web/bin/python -u /opt/ml/recsys12/Backend/db/load_json_data.py > /opt/ml/db.log &
    base_json_dir = os.path.join(os.path.dirname(__file__), 'datas', 'json')
    base_tsv_dir = os.path.join(os.path.dirname(__file__), 'datas', 'tsv')


    users_df, ratings_df = preprocessing_rating_json(os.path.join(base_json_dir, 'Books.json'))
    book_df = preprocessing_book_meta_json(
        file_path=os.path.join(base_json_dir, 'meta_Books.json'), 
        img_etc_path=os.path.join(base_tsv_dir, 'Book.tsv'))
    
    genre_df, book_genre_df = preprocessing_book_genre(
        genre_path=os.path.join(base_tsv_dir, 'Genre.tsv'),
        book_genre_path=os.path.join(base_tsv_dir, 'Book_Genre.tsv'))

    author_df, book_author_df = preprocessing_book_author(
        author_path=os.path.join(base_tsv_dir, 'Author.tsv'),
        book_autor_path=os.path.join(base_tsv_dir, 'Book_Author.tsv'))

    inference_df = preprocessing_inference(inference_path=os.path.join(base_tsv_dir, "output.csv"))
        


    df_datas = [users_df, book_df, genre_df, author_df, inference_df, book_genre_df, book_author_df, ratings_df]
    table_names = ['users', 'books', 'genres', 'authors', 'inference', 'book_genres', 'book_authors', 'ratings']

    for df, table_name in zip(df_datas, table_names):
        print(f'load {table_name}...')
        start_time = time.time()
        insert_datas(df=df, engine=engine, table_name=table_name)
        take_time = time.time() - start_time
        print(f'Done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')