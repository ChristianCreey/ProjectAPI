import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqliteName = 'movies.sqlite'
basedir = os.path.dirname(os.path.realpath(__file__))
databaseurl = f"sqlite:///{os.path.join(basedir, sqliteName)}"

engine = create_engine(databaseurl, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()