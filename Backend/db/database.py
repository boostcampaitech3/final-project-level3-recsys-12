import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
DATABASE_URL = f"postgresql://{os.environ['db_username']}:{os.environ['db_password']}@{os.environ['db_ip']}/{os.environ['db_name']}"
engine = create_engine(
    DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()