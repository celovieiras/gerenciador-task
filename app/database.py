import typing
from contextlib import contextmanager
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

load_dotenv()

class Config:
    DATABASE_USER = getenv('DATABASE_USER')
    DATABASE_PASSWORD = getenv('DATABASE_PASSWORD')
    DATABASE_HOST = getenv('DATABASE_HOST')
    DATABASE_PORT = getenv('DATABASE_PORT')
    DATABASE_NAME = getenv('DATABASE_NAME')
    DATABASE_TYPE = getenv('DATABASE_TYPE')
    @staticmethod
    def get_database_url():
        if Config.DATABASE_TYPE == 'sqlite':
            return f'sqlite:///./database.db'
        if Config.DATABASE_TYPE == 'postgresql':
            return f'postgresql://{Config.DATABASE_USER}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_HOST}:{Config.DATABASE_PORT}/{Config.DATABASE_NAME}'
        raise ValueError('Invalid database type')

engine = create_engine(Config.get_database_url(), echo=False,
                       connect_args={'check_same_thread': False} if Config.DATABASE_TYPE == 'sqlite' else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@contextmanager
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()