import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()

engine = create_engine(os.getenv('CONNECTION_STRING'), pool_size=50, max_overflow=0, pool_timeout=8)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
