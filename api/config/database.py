from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:p4ssw0rd@db:3306/finance_db"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
