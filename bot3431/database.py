import sqlalchemy
from sqlalchemy import insert, create_engine, select, update, text
# from sqlalchemy.orm import Session
from  cred import *


engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}")

