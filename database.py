from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DB_URL = "mysql+pymysql://root:naJL9!2d@localhost/Digital_Wallet" 


#using mysql ://username:password@servername/db name

engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit = False,bind = engine)


Base = declarative_base()



