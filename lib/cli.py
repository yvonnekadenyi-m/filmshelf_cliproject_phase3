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


def get_current_user(session):
    """Helper to get or select current user"""
    users = session.query(User).all()
    if not users:
        print("\n❌ No users found! Please create a user first (Option 1).")
        return None
    
    print("\n👥 Available Users:")
    for u in users:
        print(f"  {u.id}. {u.name}")

    while True:
        try:
            user_id = int(input("\nEnter user ID: "))
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                return user
            print("❌ Invalid user ID! Try again.")
        except ValueError:
            print("❌ Please enter a number!")


def main():
    """Main CLI loop"""
    # Initialize database
    init_db()

    current_user = None
    session = Session()
    
    while True:
        display_menu()
        
        if current_user:
            print(f"\n✨ Logged in as: {current_user.name}")            
        
        choice = input("\nEnter your choice: ").strip()
        
        # USER MANAGEMENT
        if choice == "1":
            name = input("\nEnter user name: ").strip()
            if name:
                create_user(name)
            else:
                print("❌ Name cannot be empty!")

        elif choice == "2":
            list_users()
        
        elif choice == "3":
            try:
                user_id = int(input("\nEnter user ID to delete: "))
                delete_user(user_id)
                if current_user and current_user.id == user_id:
                    current_user = None
            except ValueError:
                print("❌ Please enter a valid number!")

        elif choice == "4":
            current_user = get_current_user(session)
            if current_user:
                print(f"✅ Switched to user: {current_user.name}")


        elif choice == "5":
            if not current_user:
                print("❌ Please select a user first (Option 4)!")
                continue
            
            title = input("\nEnter movie title: ").strip()
            if not title:
                print("❌ Title cannot be empty!")
                continue

            genre = input("Enter genre (optional): ").strip() or None
            year_input = input("Enter year (optional): ").strip()
            year = int(year_input) if year_input.isdigit() else None
            
            movie = add_movie(title, genre, year)
            if movie:
                add_to_watchlist(current_user.id, movie.id)  


        elif choice == "6":
            if not current_user:
                print("❌ Please select a user first (Option 4)!")
                continue
            list_user_movies(current_user.id)


        elif choice == "7":
            if not current_user:
                print("❌ Please select a user first (Option 4)!")
                continue
            
            list_user_movies(current_user.id)
            try:
                review_id = int(input("\nEnter Review ID to mark as watched: "))
                mark_watched(review_id)
            except ValueError:
                print("❌ Please enter a valid number!")   


        elif choice == "8":
            if not current_user:
                print("❌ Please select a user first (Option 4)!")
                continue

            list_user_movies(current_user.id)
            try:
                review_id = int(input("\nEnter Review ID to remove: "))
                delete_from_watchlist(review_id)
            except ValueError:
                print("❌ Please enter a valid number!")
                 
                        
