from datetime import datetime
import re
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, validates
from models import Base, CRUDMixin

class User(CRUDMixin, Base):
    tablename = "users"


id = Column(Integer, primary_key=True)
username = Column(String(80), unique=True, nullable=False, index=True)
email = Column(String(255), unique=True)
created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

@validates("username")
def validate_username(self, _, value):
    cleaned = (value or "").strip()
    if not cleaned:
        raise ValueError("Username cannot be empty.")
    if len(cleaned) > 80:
        raise ValueError("Username must be 80 characters or less.")
    return cleaned

@validates("email")
def validate_email(self, _, value):
    if value is None:
        return value
    cleaned = value.strip()
    if cleaned and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", cleaned):
        raise ValueError("Email must be a valid address.")
    return cleaned or None

def __repr__(self):
    return f"<User id={self.id} username={self.username!r}>"