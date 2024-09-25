import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class DB:

    def __init__(self):
        db_username = os.environ.get("POSTGRES_USER")
        db_password = os.environ.get("POSTGRES_PASSWORD")
        db_host = os.environ.get("POSTGRES_HOST")
        db_port = os.environ.get("POSTGRES_PORT")
        db_name = os.environ.get("POSTGRES_DBNAME")

        db_url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(db_url)
        self.Session = sessionmaker(bind=engine)

    def get_session(self):
        return self.Session()
    
    def close_session(self, session):
        session.close()
