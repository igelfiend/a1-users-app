from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import config


app = FastAPI()
engine = create_engine(config.get_settings().database_url, echo=True)
Session = sessionmaker(engine)
