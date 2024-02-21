from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL = "sqlite:///institution_db.db"
engine = create_engine(URL)
Session = sessionmaker(bind = engine)
session = Session()
