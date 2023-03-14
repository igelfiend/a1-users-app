from fastapi import FastAPI
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

import os, sys
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)


app = FastAPI()

connect_url = os.environ["DATABASE_URL"]

engine = create_engine(connect_url, echo=True)
con = engine.connect()
Session = sessionmaker(engine)
