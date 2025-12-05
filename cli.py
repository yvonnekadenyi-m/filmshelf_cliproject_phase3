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