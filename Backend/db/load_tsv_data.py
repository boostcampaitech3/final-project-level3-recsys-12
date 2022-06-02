import os, sys, time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
from db.database import engine
from db.crud import pwd_context

from typing import List


def make_books_meta_df(
    user_path: str,
    author_path: str,
    genre_path: str,
    book_autor_path: str,
    book_genre_path: str,
    book_path: str,
    rating_path: str,
    inference_path: str) -> List[pd.DataFrame]:
    
    user_df = pd.read_csv(user_path, sep='\t')
    user_df.drop_duplicates(['id'], keep='first', ignore_index=True, inplace=True)
    author_df = pd.read_csv(author_path, sep='\t')
    genre_df = pd.read_csv(genre_path, sep='\t')
    book_autor_df = pd.read_csv(book_autor_path, sep='\t')
    book_genre_df = pd.read_csv(book_genre_path, sep='\t')
    book_df = pd.read_csv(book_path, sep='\t')
    rating_df = pd.read_csv(rating_path, sep='\t')
    inference_df = pd.read_csv(inference_path)

    hashed_password = pwd_context.hash('test')
    user_df['hashed_password'] = hashed_password
    book_df['publication_year'] = book_df.apply(
                                    lambda row: 0 if row['publication_year']=='None' else row['publication_year'][:4],
                                    axis=1
                                )
                                
    rating_df.sort_values(['rating'], ascending=False, inplace=True)
    rating_df.drop_duplicates(subset=['item', 'user'], keep='first', inplace=True)
    rating_df.reset_index(drop=True)
        

    return [user_df, author_df, genre_df, book_df, book_autor_df, book_genre_df, rating_df, inference_df]


def insert_datas(df: pd.DataFrame, engine, table_name: str) -> None:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )


if __name__ == '__main__':
    # excute: nohup /opt/conda/envs/web/bin/python -u /opt/ml/recsys12/Backend/db/load_tsv_data.py > /opt/ml/db.log &
    base_dir = os.path.join(os.path.dirname(__file__), 'datas', 'tsv')

    user_path = os.path.join(base_dir, 'User_Info.tsv')
    author_path = os.path.join(base_dir, 'Author.tsv')
    genre_path = os.path.join(base_dir, 'Genre.tsv')
    book_autor_path = os.path.join(base_dir, 'Book_Author.tsv')
    book_genre_path = os.path.join(base_dir, 'Book_Genre.tsv')
    book_path = os.path.join(base_dir, 'Book.tsv')
    rating_path = os.path.join(base_dir, 'Rating.tsv')
    inference_path = os.path.join(base_dir, "output.csv")

    book_meta_dfs = make_books_meta_df(
        user_path,
        author_path,
        genre_path,
        book_autor_path,
        book_genre_path,
        book_path,
        rating_path,
        inference_path,
    )

    df_datas = list()
    df_datas.extend(book_meta_dfs)
    table_names = ['users', 'authors', 'genres', 'books', 'book_authors', 'book_genres', 'ratings', 'inference'] 

    for df, table_name in zip([df_datas[-1]], [table_names[-1]]):
        print(f'load {table_name}...')
        start_time = time.time()
        insert_datas(df=df, engine=engine, table_name=table_name)
        take_time = time.time() - start_time
        print(f'Done! {int(take_time//3600)}h {int((take_time % 3600) // 60)}m {int(take_time % 60)}s')