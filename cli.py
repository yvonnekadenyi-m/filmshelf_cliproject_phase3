from tabulate import tabulate
from database import SessionLocal, init_db
from models import User, Movie, Review, Genre

def get_session():
    """Context-managed session generator."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        print(f"Error: {exc}")
    finally:
        session.close()

def prompt_nonempty(message):
    """Ask until a non-empty string is entered."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty. Try again.")

def prompt_int(message, lo=None, hi=None):
    """Ask until a valid integer is entered (with optional limits)."""
    while True:
        try:
            number = int(input(message).strip())
            if lo is not None and number < lo:
                print(f"Value must be ≥ {lo}")
                continue
            if hi is not None and number > hi:
                print(f"Value must be ≤ {hi}")
                continue
            return number
        except ValueError:
            print("Enter a valid integer.")

def choose_from_list(items, label=str, allow_skip=False):
    """Show a list and let the user choose an item."""
    if not items:
        print("Nothing to choose from.")
        return None      


    table = [(i + 1, label(x)) for i, x in enumerate(items)]
print(tabulate(table, headers=["#", "Choice"], tablefmt="github"))

if allow_skip:
    print("0. Skip")

choice = prompt_int("Select: ", 0 if allow_skip else 1, len(items))
if choice == 0 and allow_skip:
    return None
return items[choice - 1] 


def add_genre():
    name = prompt_nonempty("Genre name: ")
    for session in get_session():
        existing = session.query(Genre).filter_by(name=name).first()
        if existing:
            print("Genre already exists.")
            return
        try:
            Genre.create(session, name=name)
            print(f"Genre '{name}' added.")
        except ValueError as exc:
            print(exc)

def list_genres():
    for session in get_session():
        genres = Genre.get_all(session)
        if not genres:
            print("No genres found.")
            return
        print(tabulate([(g.id, g.name) for g in genres], headers=["ID", "Genre"], tablefmt="github"))

def delete_genre():
    for session in get_session():
        genres = Genre.get_all(session)
        if not genres:
            print("No genres to delete.")
            return
        genre = choose_from_list(genres, lambda g: f"{g.name} (id={g.id})")
        if not genre:
            return
        if genre.movies:
            print("Cannot delete a genre that still has movies.")
            return
        Genre.delete(session, genre)
        print(f"Genre '{genre.name}' deleted.")

def find_genre_by_name():
    name = prompt_nonempty("Genre name: ")
    for session in get_session():
        genre = session.query(Genre).filter(Genre.name.ilike(f"%{name}%")).all()
        if not genre:
            print("No matching genres.")
            return
        print(tabulate([(g.id, g.name) for g in genre], headers=["ID", "Genre"], tablefmt="github"))

def view_movies_for_genre():
    for session in get_session():
        genres = Genre.get_all(session)
        genre = choose_from_list(genres, lambda g: f"{g.name} (id={g.id})")
        if not genre:
            return
        movies = genre.movies
        if not movies:
            print("No movies for this genre.")
            return
        print(tabulate([(m.id, m.title) for m in movies], headers=["ID", "Title"], tablefmt="github"))            


def add_movie():
    title = prompt_nonempty("Movie title: ")
    genre_name = prompt_nonempty("Genre: ")

    for session in get_session():
    genre = session.query(Genre).filter_by(name=genre_name).first()
    if not genre:
        genre = Genre.create(session, name=genre_name)

    exists = session.query(Movie).filter_by(title=title, genre_id=genre.id).first()
    if exists:
        print("This movie already exists.")
        return

    try:
        Movie.create(session, title=title, genre=genre)
        print(f"'{title}' added under genre '{genre_name}'.")
    except ValueError as exc:
        print(exc)
def list_movies():
    for session in get_session():
        movies = (
            session.query(Movie)
            .outerjoin(Genre)
            .with_entities(Movie.id, Movie.title, Genre.name)
            .all()
        )
        if not movies:
            print("No movies found.")
        else:
            print(tabulate(movies, headers=["ID", "Title", "Genre"], tablefmt="github"))


def delete_movie():
    for session in get_session():
        movies = Movie.get_all(session)
        if not movies:
            print("No movies found.")
            return
        movie = choose_from_list(movies, lambda m: f"{m.title} (id={m.id})")
        if not movie:
            return
        Movie.delete(session, movie)
        print(f"'{movie.title}' deleted.")

def find_movie_by_title():
    title = prompt_nonempty("Title search: ")
    for session in get_session():
        matches = session.query(Movie).filter(Movie.title.ilike(f"%{title}%")).all()
        if not matches:
            print("No matching movies.")
            return
        rows = [(m.id, m.title, m.genre.name if m.genre else "-") for m in matches]
        print(tabulate(rows, headers=["ID", "Title", "Genre"], tablefmt="github"))

def view_reviews_for_movie():
    for session in get_session():
        movie = choose_from_list(Movie.get_all(session), lambda m: f"{m.title} (id={m.id})")
        if not movie:
            return
        reviews = movie.reviews
        if not reviews:
            print("No reviews for this movie.")
            return
        rows = [(r.id, r.user.username, r.rating, r.comment or "-") for r in reviews]
        print(tabulate(rows, headers=["Review ID", "User", "Rating", "Comment"], tablefmt="github"))

def list_movies_by_genre():
    for session in get_session():
        genre = choose_from_list(Genre.get_all(session), lambda g: f"{g.name} (id={g.id})")
        if not genre:
            return
        movies = genre.movies
        if not movies:
            print("No movies in this genre.")
            return
        print(tabulate([(m.id, m.title) for m in movies], headers=["ID", "Title"], tablefmt="github"))

---------------- User Commands ----------------
def add_user():
    username = prompt_nonempty("Username: ")
    email = input("Email (optional): ").strip() or None

for session in get_session():
    if session.query(User).filter_by(username=username).first():
        print("Username already exists.")
        return
    if email and session.query(User).filter_by(email=email).first():
        print("Email already exists.")
        return
    try:
        User.create(session, username=username, email=email)
        print(f"User '{username}' added.")
    except ValueError as exc:
        print(exc)
def list_users():
    for session in get_session():
        users = User.get_all(session)
        if not users:
            print("No users found.")
        else:

             table = [(u.id, u.username, u.email or "-") for u in users]
            print(tabulate(table, headers=["ID", "Username", "Email"], tablefmt="github"))

def delete_user():
    for session in get_session():
        users = User.get_all(session)
        if not users:
            print("No users found.")
            return
        user = choose_from_list(users, lambda u: f"{u.username} (id={u.id})")
        if not user:
            return
        if user.reviews:
            print("User has reviews; deleting will remove their reviews too.")
        User.delete(session, user)
        print(f"'{user.username}' deleted.")

def find_user():
    username = prompt_nonempty("Username search: ")
    for session in get_session():
        matches = session.query(User).filter(User.username.ilike(f"%{username}%")).all()
        if not matches:
            print("No matching users.")
            return
        rows = [(u.id, u.username, u.email or "-") for u in matches]
        print(tabulate(rows, headers=["ID", "Username", "Email"], tablefmt="github"))

def view_user_reviews():
    for session in get_session():
        user = choose_from_list(User.get_all(session), lambda u: f"{u.username} (id={u.id})")
        if not user:
            return
        reviews = user.reviews
        if not reviews:
            print("User has not added any reviews.")
            return
        rows = [(r.id, r.movie.title, r.rating, r.comment or "-") for r in reviews]
        print(tabulate(rows, headers=["Review ID", "Movie", "Rating", "Comment"], tablefmt="github"))


def add_review():
    for session in get_session():
        user = choose_from_list(User.get_all(session), lambda u: f"{u.username} (id={u.id})")
        movie = choose_from_list(Movie.get_all(session), lambda m: f"{m.title} (id={m.id})")

    if not user or not movie:
        return

    if session.query(Review).filter_by(user_id=user.id, movie_id=movie.id).first():
        print("Already reviewed this movie.")
        return

    rating = prompt_int("Rating (1-5): ", 1, 5)
    comment = input("Comment: ").strip() or None

    try:
        Review.create(session, user=user, movie=movie, rating=rating, comment=comment)
        print(f"{user.username} rated '{movie.title}' {rating}/5.")
    except ValueError as exc:
        print(exc)

    if not user or not movie:
        return

    if session.query(Review).filter_by(user_id=user.id, movie_id=movie.id).first():
        print("Already reviewed this movie.")
        return

    rating = prompt_int("Rating (1-5): ", 1, 5)
    comment = input("Comment: ").strip() or None

    try:
        Review.create(session, user=user, movie=movie, rating=rating, comment=comment)
        print(f"{user.username} rated '{movie.title}' {rating}/5.")
    except ValueError as exc:
        print(exc)

def list_reviews():
    for session in get_session():
        reviews = (
            session.query(Review)
            .join(User)
            .join(Movie)
            .with_entities(Review.id, User.username, Movie.title, Review.rating, Review.comment, Review.created_at)
            .all()
        )
        if not reviews:
            print("No reviews found.")
        else:
            print(tabulate(reviews, headers=["ID", "User", "Movie", "Rating", "Comment", "Created"], tablefmt="github"))

def delete_review():
    for session in get_session():
        reviews = Review.get_all(session)
        if not reviews:
            print("No reviews to delete.")
            return
        review = choose_from_list(
            reviews, lambda r: f"{r.id}: {r.user.username} -> {r.movie.title} ({r.rating}/5)"
        )
        if not review:
            return
        Review.delete(session, review)
        print("Review deleted.")

def find_review_by_id():
    review_id = prompt_int("Review ID: ", lo=1)
    for session in get_session():
        review = Review.find_by_id(session, review_id)
        if not review:
            print("Review not found.")
            return
        rows = [
            (
                review.id,
                review.user.username,
                review.movie.title,
                review.rating,
                review.comment or "-",
                review.created_at,
            )
        ]
        print(tabulate(rows, headers=["ID", "User", "Movie", "Rating", "Comment", "Created"], tablefmt="github"))

def run_menu(title, options):
    """Generic loop to render a menu and trigger handlers."""
    while True:
        print(f"\n--- {title} ---")
        for number, (label, _) in options.items():
            print(f"{number}. {label}")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            return
        action = options.get(choice)
        if not action:
            print("Invalid option. Try again.")
            continue
        action1

def main_menu():
    while True:
        print("\n=== Movie Watchlist CLI ===")
        print("1. Movies")
        print("2. Genres")
        print("3. Users")
        print("4. Reviews")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        if choice == "1":
            run_menu(
                "Movies",
                {
                    "1": ("Add movie", add_movie),
                    "2": ("List movies", list_movies),
                    "3": ("Delete movie", delete_movie),
                    "4": ("Find movie by title", find_movie_by_title),
                    "5": ("View reviews for movie", view_reviews_for_movie),
                    "6": ("List movies by genre", list_movies_by_genre),
                    "0": ("Back", lambda: None),
                },
            )
        elif choice == "2":
            run_menu(
                "Genres",
                {
                    "1": ("Add genre", add_genre),
                    "2": ("List genres", list_genres),
                    "3": ("Delete genre", delete_genre),
                    "4": ("Find genre by name", find_genre_by_name),
                    "5": ("View movies in genre", view_movies_for_genre),
                    "0": ("Back", lambda: None),
                },
            )
        elif choice == "3":
            run_menu(
                "Users",
                {
                    "1": ("Add user", add_user),
                    "2": ("List users", list_users),
                    "3": ("Delete user", delete_user),
                    "4": ("Find user", find_user),
                    "5": ("View user reviews", view_user_reviews),
                    "0": ("Back", lambda: None),
                },
            )
        elif choice == "4":
            run_menu(
                "Reviews",
                {
                    "1": ("Add review", add_review),
                    "2": ("List reviews", list_reviews),
                    "3": ("Delete review", delete_review),
                    "4": ("Find review by ID", find_review_by_id),
                    "0": ("Back", lambda: None),
                },
            )
        else:
            print("Invalid option. Try again.")

def main():
    init_db()
    main_menu()

if name == "main":
    main()

    