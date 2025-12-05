from lib.models import Session, User, Movie, Review, init_db

def seed_data():
    """Add sample data to the database"""
    init_db()
    session = Session()
    
    try:
        # Create users
        user1 = User(name="Alice")
        user2 = User(name="Bob")
        session.add_all([user1, user2])
        session.commit()
        