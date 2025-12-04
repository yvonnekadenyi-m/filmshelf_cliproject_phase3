from lib.models import Session, User, Movie, Review
from tabulate import tabulate

def create_user(name):
    """Create a new user"""
    session = Session()
    try:
        user = User(name=name)
        session.add(user)
        session.commit()
        print(f"✅ User '{name}' created successfully!")

        
