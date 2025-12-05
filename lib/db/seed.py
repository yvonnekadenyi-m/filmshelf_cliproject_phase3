from lib.models import Session, User, Movie, Review, init_db

def seed_data():
    """Add sample data to the database"""
    init_db()
    session = Session()
    