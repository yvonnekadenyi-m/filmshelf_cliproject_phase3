from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    reviews = relationship('Review', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    reviews = relationship('Review', back_populates='movie', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}', year={self.year})>"

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    watched = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)

    user = relationship('User', back_populates='reviews')
    movie = relationship('Movie', back_populates='reviews')

    def __repr__(self):
        return f"<Review(id={self.id}, user_id={self.user_id}, movie_id={self.movie_id}, watched={self.watched})>"

    def init_db():
        Base.metadata.create_all(engine)
        print("✅ Database initialized!")
    
    if __name__ == "__main__":
        init_db()