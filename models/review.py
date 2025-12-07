from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship, validates
from . import Base, CRUDMixin


class Review(CRUDMixin, Base):
    __tablename__ = "reviews"
    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name="ck_review_rating_range"),
        UniqueConstraint("user_id", "movie_id", name="uq_user_movie_review"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")

    @validates("rating")
    def validate_rating(self, _, value):
        if value is None:
            raise ValueError("Rating is required.")
        if not (1 <= int(value) <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return int(value)

    @validates("comment")
    def validate_comment(self, _, value):
        if value is None:
            return None
        cleaned = value.strip()
        if len(cleaned) > 500:
            raise ValueError("Comment must be 500 characters or less.")
        return cleaned or None

    def __repr__(self):
        return f"<Review id={self.id} user_id={self.user_id} movie_id={self.movie_id} rating={self.rating}>"
