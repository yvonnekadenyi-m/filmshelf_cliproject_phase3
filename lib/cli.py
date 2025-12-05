from lib.models import init_db, Session, User
from lib.helpers import (
    create_user, list_users, delete_user,
    add_movie, add_to_watchlist, list_user_movies,
    mark_watched, add_review, list_all_reviews,
    delete_from_watchlist
)

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("🎬  FILMSHELF - YOUR PERSONAL MOVIE WATCHLIST  🎬")
    print("="*50)