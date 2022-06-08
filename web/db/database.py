import os, yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config_db.yaml')
with open(CONFIG_PATH) as config:
    conf = yaml.load(config, Loader=yaml.FullLoader)
    DATABASE_URL = f"postgresql://{conf['db_username']}:{conf['db_password']}@{conf['db_ip']}/{conf['db_name']}"

engine = create_engine(
    DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()