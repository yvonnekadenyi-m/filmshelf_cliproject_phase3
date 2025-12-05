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

def list_users():
    """Display all users"""
    session = Session()
    try:
        users = session.query(User).all()
        if not users:
            print("📭 No users found.")
            return        
        
        table = [[user.id, user.name] for user in users]
        print(tabulate(table, headers=["ID", "Name"], tablefmt="grid"))
    finally:
        session.close()  


def delete_user(user_id):
    """Delete a user"""
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print(f"❌ User with ID {user_id} not found!")
            return False
        
        session.delete(user)
        session.commit()
        print(f"✅ User '{user.name}' deleted successfully!")
        return True
    
    except Exception as e:
        session.rollback()
        print(f"❌ Error deleting user: {e}")
        return False
    
    finally:
        session.close()


def add_movie(title, genre=None, year=None):
    """Add a movie to the database (or return existing)"""
    session = Session()
    try:

        movie = session.query(Movie).filter_by(title=title).first()
        if movie:
            print(f"ℹ️  Movie '{title}' already exists in database.")
            return movie
        
        movie = Movie(title=title, genre=genre, year=year)
        session.add(movie)
        session.commit()
        print(f"✅ Movie '{title}' added to database!")
        return movie