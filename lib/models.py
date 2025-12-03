from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()

