from lib.models import Session, User, Movie, Review
from tabulate import tabulate

def create_user(name):
    """Create a new user"""
    session = Session()
    try:
        existing = session.query(User).filter_by(name=name).first()
        if existing:
            print(f"❌ User '{name}' already exists!")
            return None

        user = User(name=name)
        session.add(user)
        session.commit()
        print(f"✅ User '{name}' created successfully!")
        return user

    except Exception as e:
        session.rollback()
        print(f"❌ Error creating user: {e}")
        return None
    finally:
        session.close()