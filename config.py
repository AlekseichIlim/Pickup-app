import os
from dotenv import load_dotenv


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ADMINS = [1892638646, ]


load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")
PICKUP_BOT_TOKEN = os.getenv("PICKUP_BOT_TOKEN")

DEBUG = True

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()