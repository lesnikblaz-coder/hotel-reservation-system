from sqlalchemy import text
from database import engine, SessionLocal


def test_engine_connection():
    with engine.connect() as conn:
        assert conn.execute(text("SELECT 1")).scalar() == 1


def test_session_connection():
    db = SessionLocal()
    try:
        assert db.execute(text("SELECT 1")).scalar() == 1
    finally:
        db.close()