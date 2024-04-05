from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(id=user.id, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
