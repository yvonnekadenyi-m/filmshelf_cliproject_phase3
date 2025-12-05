from tabulate import tabulate
from database import SessionLocal, init_db
from models import User, Movie, Review, Genre

def get_session():
    """Context-managed session generator."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        print(f"Error: {exc}")
    finally:
        session.close()