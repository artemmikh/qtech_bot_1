import datetime
import os

from sqlalchemy import Column, String, Text, Boolean, DateTime, create_engine, \
    Integer
from sqlalchemy_utils import URLType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('BOT_DATABASE_URL'), echo=True)
Base = declarative_base()


class Button(Base):
    __tablename__ = 'button'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    is_moscow = Column(Boolean, default=True)
    text = Column(Text())
    picture = Column(URLType, nullable=True)
    file = Column(URLType, nullable=True)
    is_department = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


Session = sessionmaker(bind=engine)
session = Session()
