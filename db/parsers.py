import csv
from . import models
from .database import SessionLocal, engine


db = SessionLocal()

models.Base.metadata.create_all(bind=engine)


with open("raw_data/Users.csv", "r") as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        try:
            db_record = models.User(
                id=row["User-ID"],
                email=row["E-mail"],
                hashed_password=row["Password"],
                name=row["Name"],
            )
        except Exception as E:
            print(E)
            print(f'{row["User-ID"]}')

        db.add(db_record)
    db.commit()


with open("raw_data/Books.csv", "r") as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        try:
            db_record = models.Book(
                id=row["ISBN"],
                title=row["Book-Title"],
                # author=row["Book-Author"],
                # category=row["Category"],
                publication_year=int(row["Year-Of-Publication"]),
                description=row["Description"],
                image_URL=row["Image-URL-S"],
            )
        except:
            print('Book Error')

        db.add(db_record)

    db.commit()

with open("raw_data/Authors.csv", "r") as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        try:
            db_record = models.Author(
                id=row["ID"],
                name=row["Book-Author"],
            )
        except:
            print('Author Error')

        db.add(db_record)

    db.commit()

with open("raw_data/Book_Author.csv", "r") as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        try:
            db_record = models.BookAuthor(
                book_id=row["ISBN"],
                author_id=row["Book-Author"],
            )
        except:
            print('BookAuthor Error')

        db.add(db_record)

    db.commit()


# with open("raw_data/Genres.csv", "r") as f:
#     csv_reader = csv.DictReader(f)

#     for row in csv_reader:
#         try:
#             db_record = models.Genre(
#                 id=row["ID"],
#                 name=row["Name"],
#             )
#         except:
#             print('Genre Error')

#         db.add(db_record)

#     db.commit()


# with open("raw_data/Book_Genre.csv", "r") as f:
#     csv_reader = csv.DictReader(f)

#     for row in csv_reader:
#         try:
#             db_record = models.BookGenre(
#                 book_id=row["ISBN"],
#                 genre_id=row["Genre"],
#             )
#         except:
#             print('BookGenre Error')

#         db.add(db_record)

#     db.commit()

with open("raw_data/Ratings.csv", "r") as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        try:
            db_record = models.Rating(
                user=row["User-ID"],
                item=row["ISBN"],
                rating=row["Book-Rating"],
            )
        except:
            print('Rating Error')

        db.add(db_record)

    db.commit()

db.close()