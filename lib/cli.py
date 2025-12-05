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
    print("\n👤 USER MANAGEMENT:")
    print("  1. Create User")
    print("  2. List All Users")
    print("  3. Delete User")
    print("  4. Select Current User")
    print("\n🎥 WATCHLIST MANAGEMENT:")
    print("  5. Add Movie to Watchlist")
    print("  6. View My Watchlist")
    print("  7. Mark Movie as Watched")
    print("  8. Remove from Watchlist")
    print("\n📝 REVIEWS:")
    print("  9. Add/Edit Review")
    print("  10. View My Reviews")
    print("\n  0. Exit")
    print("="*50)