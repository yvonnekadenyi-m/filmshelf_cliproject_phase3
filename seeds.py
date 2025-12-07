
from database import init_db, SessionLocal
from models import User, Genre, Movie, Review


def seed():
    init_db()
    session = SessionLocal()
    try:
        # Simple idempotent-ish seed: only create if missing
        genres = {
            "Sci-Fi": session.query(Genre).filter_by(name="Sci-Fi").first()
            or Genre.create(session, name="Sci-Fi"),
            "Drama": session.query(Genre).filter_by(name="Drama").first()
            or Genre.create(session, name="Drama"),
        }

        movies = {
            "Interstellar": session.query(Movie)
            .filter_by(title="Interstellar", genre_id=genres["Sci-Fi"].id)
            .first()
            or Movie.create(session, title="Interstellar", genre=genres["Sci-Fi"]),
            "The Martian": session.query(Movie)
            .filter_by(title="The Martian", genre_id=genres["Sci-Fi"].id)
            .first()
            or Movie.create(session, title="The Martian", genre=genres["Sci-Fi"]),
            "The Social Network": session.query(Movie)
            .filter_by(title="The Social Network", genre_id=genres["Drama"].id)
            .first()
            or Movie.create(session, title="The Social Network", genre=genres["Drama"]),
        }

        users = {
            "alice": session.query(User).filter_by(username="alice").first()
            or User.create(session, username="alice", email="alice@example.com"),
            "bob": session.query(User).filter_by(username="bob").first()
            or User.create(session, username="bob", email="bob@example.com"),
        }

        # Reviews (avoid duplicates)
        if not session.query(Review).filter_by(user_id=users["alice"].id, movie_id=movies["Interstellar"].id).first():
            Review.create(
                session,
                user=users["alice"],
                movie=movies["Interstellar"],
                rating=5,
                comment="Mind-blowing visuals.",
            )
        if not session.query(Review).filter_by(user_id=users["bob"].id, movie_id=movies["The Martian"].id).first():
            Review.create(
                session,
                user=users["bob"],
                movie=movies["The Martian"],
                rating=4,
                comment="Funny and tense.",
            )

        session.commit()
        print("Seed complete.")
    finally:
        session.close()


if __name__ == "__main__":
    seed()