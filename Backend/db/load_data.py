import os
import pandas as pd
from . import database

from typing import Tuple


def preprocessing_user_file(file_path: str) -> pd.DataFrame:
    users = pd.read_csv(file_path)
    users.rename(columns={'User-ID':'user_id', 'Location':'location', 'Age':'age'}, inplace=True)
    users['user_id'] = convert_id_2_email_form(users['user_id'])
    users['age'] = users['age'].fillna(0).astype(int)
    add_cloumns_with_nullstr_value(users, ('hashed_password', 'name'))
    user_location = split_location(users['location'])
    user_info = pd.concat([users, user_location], axis=1).drop(labels='location', axis=1)

    return user_info


def convert_id_2_email_form(user_id: pd.Series) -> pd.Series:
    user_id = user_id.astype(str)
    user_id = user_id + '@gmail.com'

    return user_id


def add_cloumns_with_nullstr_value(df: pd.DataFrame, columns: Tuple[str]) -> None:
    for column in columns:
        df[column] = ''


def split_location(location_series: pd.Series) -> pd.Series:
    user_location = location_series.str.split(',', expand=True)
    user_location.drop(labels=[3, 4,5,6,7,8], axis=1, inplace=True)
    user_location.rename(columns={0:'city', 1:'state', 2:'country'}, inplace=True)
    
    return user_location


def preprocessing_book_file(file_path: str) -> pd.DataFrame:
    books = pd.read_csv(file_path, encoding='cp949')
    books.rename(columns={
                    'ISBN': 'isbn',
                    'Book-Title': 'title',
                    'Book-Author': 'author',
                    'Publisher': 'publisher',
                    'Year-Of-Publication': 'publication_year',
                    'Image-URL-S': 'image_S_URL',
                    'Image-URL-M': 'image_M_URL',
                    'Image-URL-L': 'image_L_URL',
                    }, inplace=True)
    
    books['isbn'] = books.apply(
                        lambda row: row.image_S_URL.split('/')[5].split('.')[0]
                        ,axis=1)
    
    books.drop_duplicates(['isbn'], keep='first', ignore_index=True, inplace=True)
    
    return books


def preprocessing_rating_file(file_path: str) -> pd.DataFrame:
    ratings = pd.read_csv(file_path)
    ratings.rename(columns={
                    'User-ID': 'user_id',
                    'ISBN': 'isbn',
                    'Book-Rating': 'rating'
                    }, inplace=True)
    ratings['user_id'] = convert_id_2_email_form(ratings['user_id'])

    non_user_id_list = []
    non_isbn_list = ['3257224281', '0600570967', '342310538', '3442437407', '033390804X', '8440682697', '3404611306', '342662429', '3453157745', '3453185323']
    drop_non_FK(ratings, non_user_id_list, non_isbn_list)
                
    return ratings


def drop_non_FK(df: pd.DataFrame, non_user_id_list: list, non_isbn_list: list) -> None:
    for non_user_id in non_user_id_list:
        df.drop(
            index=df[df.user_id==non_user_id].index,
            axis=0,
            inplace=True,
        )
        df.reset_index(drop=True, inplace=True)
    
    for non_isbn in non_isbn_list:
        df.drop(
            index=df[df.isbn==non_isbn].index,
            axis=0,
            inplace=True,
        )
        df.reset_index(drop=True, inplace=True)


def insert_datas(df: pd.DataFrame, engine, table_name: str) -> None:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )



if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    # user_info = preprocessing_user_file(os.path.join(base_dir, 'datas', 'Users.csv'))
    # book_info = preprocessing_book_file(os.path.join(base_dir, 'datas', 'Books.csv'))
    ratings = preprocessing_rating_file(os.path.join(base_dir, 'datas', 'Ratings.csv'))

    # df_datas = [user_info, book_info, ratings]
    # table_names = ['user_info', 'book_info', 'ratings']

    df_datas = [ratings]
    table_names = ['ratings']


    for df, table_name in zip(df_datas, table_names):
        print(f'load {table_name}...')
        insert_datas(df=df, engine=database.engine, table_name=table_name)
        print('Done!')