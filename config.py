import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = "mysql://root:Nata542247@localhost/aclaraciones_db"

SQLALCHEMY_TRACK_MODIFICATIONS = False
