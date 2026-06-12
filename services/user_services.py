from sqlalchemy.orm import Session

import repository
from models import User
from schemas import UserUpdate
from exceptions import UserNotFoundError

def user_get_by_id(db: Session, user_id: int) -> User:
    user = repository.get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFoundError("User does not exist.")
    return user

def user_update(db: Session, user_id: int, data: UserUpdate) -> User:
    user = user_get_by_id(db, user_id)
    return repository.user_update(db, user, data)

def users_get_all(db: Session) -> list[User]:
    return repository.get_all_users(db)

def user_delete(db: Session, user_id: int) -> None:
    user = user_get_by_id(db, user_id)
    repository.user_delete(db, user)