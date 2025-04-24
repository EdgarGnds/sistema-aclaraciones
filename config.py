import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///C:/Users/hp/Documents/sistema-aclaraciones/data/aclaraciones.db")

SQLALCHEMY_TRACK_MODIFICATIONS = False
