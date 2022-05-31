import os, gc, json, time
import pandas as pd
from .database import engine
from crud import pwd_context

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
    review_summary = []

    for data in generate_json:
        if data['asin'][0] == 'B': continue
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
    hashed_password = pwd_context.hash('test')
    users_df['hashed_password'] = hashed_password
    take_time = time.time() - start_time
    print(f'\t\tmake hashed_password done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return users_df


def make_ratings_df(users: List[str], items: List[str], ratings: List[str], reviews: List[str]) -> pd.DataFrame:
    ratings_df = pd.DataFrame()
    ratings_df['user'] = users
    ratings_df['item'] = items
    ratings_df['rating'] = ratings
    ratings_df['rating'] = ratings_df['rating'].astype('int8')
    # ratings_df['reivew'] = reviews

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
        reviews=datas_dict['review_summary'] ,   
    )
    print('\tratings df done!')
    take_time = time.time() - start_time
    print(f'preprocessing ratings json done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')

    return users_df, ratings_df


def make_df_of_meta(gen_meta, gen_img):
    isbns, img_isbns, titles, genres, img_urls = list(), list(), list(), list(), list()

    for data in gen_meta:
        if data['asin'][0] == 'B': continue
        isbns.append(data['asin'])
        titles.append(data['title'])
        genres.append(data['category'])
        # if data['description']: description.append(data['description'][0])
        # else: description.append('')
        # author.append(data['brand'])

    for data in gen_img:
        img_isbns.append(data['isbn'])
        img_urls.append(data['url'])

    books_img = pd.DataFrame()
    books_img['id'] = img_isbns
    books_img['image_URL'] = img_urls

    books = pd.DataFrame()
    books['id'] = isbns
    books['title'] = titles

    book_merge = pd.merge(books, books_img, left_on='id', right_on='id', how='left')

    return book_merge, genres


def get_meta_datas_df(file_path: str, img_file_path: str) -> pd.DataFrame:
    gen_meta_json = load_json_data(file_path)
    gen_img_json = load_json_data(img_file_path)

    books, genres = make_df_of_meta(gen_meta_json, gen_img_json)
    return books, genres


def make_df_of_genre(gen_meta, genres: list) -> Tuple[list, list]:
    genre_df = pd.DataFrame()
    split_genre = list()

    for genre in genres:
        if genre:
            split_genre.extend(genre)
    split_genre = list(set(split_genre))
    genre_df['name'] = split_genre
    genre_df['id'] = genre_df.index

    book_genre_id, book_genre_genre = list(), list()
    book_genre_df = pd.DataFrame()

    for data in gen_meta:
        if data['asin'][0] == 'B': continue
        if data['category']:
            for genre in data['category']:
                book_genre_id.append(data['asin'])
                book_genre_genre.append(split_genre.index(genre))
    
    book_genre_df['book_id'] = book_genre_id
    book_genre_df['genre_id'] = book_genre_genre

    return genre_df, book_genre_df


def get_genre_df(file_path: str, genres: list):
    gen_meta_json = load_json_data(file_path)
    genre_df, book_genre_df = make_df_of_genre(gen_meta_json, genres)
    return genre_df, book_genre_df


def preprocessing_book_meta_json(file_path: str, img_file_path: str):
    book_df, genres = get_meta_datas_df(file_path, img_file_path)
    genre_df, book_genre_df = get_genre_df(file_path, genres)
    return book_df, genre_df, book_genre_df


def insert_datas(df: pd.DataFrame, engine, table_name: str) -> None:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )


if __name__ == '__main__':
    # excute: nohup /opt/conda/envs/web/bin/python -u /opt/ml/recsys12/Backend/db/load_data.py > /opt/ml/db.log &
    base_dir = os.path.join(os.path.dirname(__file__), 'datas', 'json')
    users_df, ratings_df = preprocessing_rating_json(os.path.join(base_dir, 'Books.json'))
    book_df, genre_df, book_genre_df = preprocessing_book_meta_json(
        file_path=os.path.join(base_dir, 'Books.json'),
        img_file_path=os.path.join(base_dir, 'img_url_ver2.json'))

    df_datas = [users_df, book_df, genre_df, book_genre_df]
    table_names = ['users', 'books', 'genres', 'book_genres']

    for df, table_name in zip(df_datas, table_names):
        print(f'load {table_name}...')
        start_time = time.time()
        insert_datas(df=df, engine=engine, table_name=table_name)
        take_time = time.time() - start_time
        print(f'Done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')