import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqliteName = 'movies.sqlite'
basedir = os.path.dirname(os.path.realpath(__file__))
databaseurl = f"sqlite:///{os.path.join(basedir, sqliteName)}"

#crear la base de datos si no exite
if not os.path.exists(os.path.join(basedir, sqliteName)):
    open(os.path.join(basedir, sqliteName), 'w').close()

engine = create_engine(databaseurl, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

# Verificar si la base de datos fue creada
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tablas en la base de datos: {tables}")

#para crear la base de datos
#docker run -it --rm -p 4000:4000 -v C:\Users\60100218\Documents\ProjectAPI:/app projectapi
