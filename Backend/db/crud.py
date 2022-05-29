import os, yaml
from sqlalchemy.orm import Session
from . import models, schemas

from passlib.context import CryptContext


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config_hash.yaml')
with open(CONFIG_PATH) as config:
    conf = yaml.load(config, Loader=yaml.FullLoader)
    SECRET_KEY = conf['secret_key']
    ALGORITHM = conf['ALGORITHM']
    SCHEMES = conf['SCHEMES']

pwd_context = CryptContext(schemes=[SCHEMES], deprecated="auto")


def get_user(db: Session, id: str):
    return db.query(models.User).filter(models.User.id==id).first()


def create_user(db: Session, user: schemas.UserCreate, user_info: schemas.User):
    hashed_password = pwd_context.hash(user.password+user.id)
    db_user = models.User(
        hashed_password=hashed_password,
        **user_info.dict(),
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)