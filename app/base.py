from fastapi import FastAPI
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker


app = FastAPI()

connect_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="postgres",
    host="db",
    # port="5432",
    database="a1-users",
)
engine = create_engine(connect_url, echo=True)
con = engine.connect()
Session = sessionmaker(engine)
