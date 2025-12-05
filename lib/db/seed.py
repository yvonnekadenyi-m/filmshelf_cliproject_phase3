from lib.models import Session, User, Movie, Review, init_db

def seed_data():
    """Add sample data to the database"""
    init_db()
    session = Session()
    
    try:
        # Create users
        user1 = User(name="Alice")
        user2 = User(name="Bob")
        session.add_all([user1, user2])
        session.commit()

        movie1 = Movie(title="The Shawshank Redemption", genre="Drama", year=1994)
        movie2 = Movie(title="The Dark Knight", genre="Action", year=2008)
        movie3 = Movie(title="Inception", genre="Sci-Fi", year=2010)
        movie4 = Movie(title="Pulp Fiction", genre="Crime", year=1994)
        session.add_all([movie1, movie2, movie3, movie4])
        session.commit()
        
        review1 = Review(
            user_id=user1.id,
            movie_id=movie1.id,
            content="Amazing movie! A masterpiece.",
            rating=5,
            watched=True
        )
        
        review2 = Review(
            user_id=user1.id,
            movie_id=movie2.id,
            watched=False
        )

        review3 = Review(
            user_id=user2.id,
            movie_id=movie3.id,
            content="Mind-bending and visually stunning!",
            rating=5,
            watched=True
        )