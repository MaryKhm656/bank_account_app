from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///bank.db")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)