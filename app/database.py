import os
import dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

dotenv.load_dotenv(dotenv.find_dotenv())

engine_connection_string = '{}+{}://{}:{}@{}:{}/{}'.format(
    os.getenv('DATABASE_TYPE'),
    os.getenv('DATABASE_DRIVER'),
    os.getenv('DATABASE_USERNAME'),
    os.getenv('DATABASE_PASSWORD'),
    os.getenv('DATABASE_HOST'),
    os.getenv('DATABASE_PORT'),
    os.getenv('DATABASE_NAME')
)

ENGINE = create_engine(engine_connection_string)
BASE = declarative_base()
SESSION = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))
