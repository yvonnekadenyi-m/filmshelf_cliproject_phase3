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

        
