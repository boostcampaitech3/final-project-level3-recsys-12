from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def verification_user(db: Session, try_user: schemas.UserCreate):
    fake_hashed_password = try_user.password + "notreallyhashed"
    is_exist = db.query(models.User).filter(
                                    (models.User.user_id==try_user.user_id) &
                                    (models.User.hashed_password==fake_hashed_password)).first()

    if is_exist: return True
    else: return False


def create_user(db: Session, user: schemas.UserCreate, user_info: schemas.User):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        hashed_password=fake_hashed_password,
        **user_info.dict(),
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)