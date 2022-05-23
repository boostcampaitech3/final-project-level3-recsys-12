import csv
from . import models
from .database import SessionLocal, engine


db = SessionLocal()

models.Base.metadata.create_all(bind=engine)

with open("../../Preprocessing/Books.csv", "r") as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        try:
            db_record = models.Item(
                isbn=row["ISBN"],
                title=row["Book-Title"],
                author=row["Book-Author"],
                publisher=row["Publisher"],
                publication_year=int(row["Year-Of-Publication"]),
                image_URL=row["Image-URL-L"],
            )
        except:
            print(f'{row["ISBN"]}')
            print(f'{row["Year-Of-Publication"]}')

        db.add(db_record)

    db.commit()

db.close()