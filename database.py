from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, unique=True)
    consent = Column(Boolean, default=False)
    start_date = Column(DateTime)
    current_day = Column(Integer, default=0)
    cycle = Column(Integer, default=1)

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    day = Column(Integer)
    color = Column(String(50))
    description = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)
    cycle = Column(Integer)

# Для Heroku
DATABASE_URL = os.environ.get('DATABASE_URL', '').replace("postgres://", "postgresql://")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)