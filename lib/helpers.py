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
    
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding movie: {e}")
        return None
    
    finally:
        session.close()

def add_to_watchlist(user_id, movie_id):
    """Add a movie to user's watchlist (creates a review entry)"""
    session = Session()
    try:
        existing = session.query(Review).filter_by(
            user_id=user_id, 
            movie_id=movie_id
        ).first()
        if existing:
            print("ℹ️  Movie already in watchlist.")
            return existing
        
        review = Review(user_id=user_id, movie_id=movie_id, watched=False)
        session.add(review)
        session.commit()
        print("✅ Movie added to your watchlist!")
        return review
    
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding to watchlist: {e}")
        return None
    
    finally:
        session.close()


def list_user_movies(user_id):
    """Display all movies in a user's watchlist"""
    session = Session()
    try:
        reviews = session.query(Review).filter_by(user_id=user_id).all()
        if not reviews:
            print("📭 Your watchlist is empty.")
            return
        
        table_data = []
        for r in reviews:
            status = "✅ Watched" if r.watched else "⏳ Not Watched"
            rating = f"{r.rating}/5 ⭐" if r.rating else "No rating"
            table_data.append([
                r.id,
                r.movie.title,
                r.movie.genre or "N/A",
                r.movie.year or "N/A",
                status,
                rating
            ])


        print("\n" + tabulate(
            table_data, 
            headers=["Review ID", "Title", "Genre", "Year", "Status", "Rating"],
            tablefmt="grid"
        ))     

    finally:
        session.close()       


def mark_movie_watched(review_id, rating=None):
    """Mark a movie as watched and optionally add a rating"""
    session = Session()
    try:
        review = session.query(Review).filter_by(id=review_id).first()
        if not review:
            print(f"❌ Review with ID {review_id} not found!")
            return False
        
        review.watched = True
        if rating is not None:
            review.rating = rating
        
        session.commit()
        print(f"✅ Movie '{review.movie.title}' marked as watched!")
        return True
    
    except Exception as e:
        session.rollback()
        print(f"❌ Error updating review: {e}")
        return False
    
    finally:
        session.close()        
        
