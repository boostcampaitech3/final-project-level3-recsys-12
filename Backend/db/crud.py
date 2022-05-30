import os, yaml
from sqlalchemy.orm import Session
from zmq import PLAIN_PASSWORD
from . import models, schemas

from passlib.context import CryptContext


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config_hash.yaml')
with open(CONFIG_PATH) as config:
    conf = yaml.load(config, Loader=yaml.FullLoader)
    SECRET_KEY = conf['secret_key']
    ALGORITHM = conf['ALGORITHM']
    SCHEMES = conf['SCHEMES']
    FAKE_PASSWORD = conf['FAKE_PASSWORD']

pwd_context = CryptContext(schemes=[SCHEMES], deprecated="auto")


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate, user_info: schemas.User):
    hashed_password = pwd_context.hash(user.password+FAKE_PASSWORD)
    db_user = models.User(
        hashed_password=hashed_password,
        **user_info.dict(),
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def get_recent_item(db: Session, skip: int = 0, limit: int = 2):
    return db.query(models.Book).order_by('publication_year').offset(skip).limit(limit).all()


def get_item(db:Session, item_id: str):
    return db.query(models.Book).filter(models.Book.id == item_id).first()


def all_genres(db:Session):
    return db.query(models.Genre).all()



def get_genres(db:Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first().books


def get_item_by_genre(db:Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.id == genre_id).all()