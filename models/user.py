from datetime import datetime
import re
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, validates
from models import Base, CRUDMixin

class User(CRUDMixin, Base):
    tablename = "users"