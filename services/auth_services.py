import repository, auth

from sqlalchemy.orm import Session

from models import User
from exceptions import DuplicateEmailError, InvalidCredentialsError

def register(db: Session, email: str, password: str) -> User:
    if repository.get_user_by_email(db, email):
        raise DuplicateEmailError("Email already registered.")

    user = User(email=email, hashed_password=auth.hash_password(password))

    return repository.user_create(db, user)

def login(db: Session, email: str, password: str):
    user = repository.get_user_by_email(db, email)

    if not user or not auth.verify_password(password, user.hashed_password):
        raise InvalidCredentialsError("Invalid credentials.")

    return {
        "access_token": auth.create_access_token(user.user_id),
        "token_type": "bearer"
    }