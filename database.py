from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 

MYSQL_USER = "root"
MYSQL_PASSWORD = "Golden%401234"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "fastapi_db"

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"


engine = create_engine(DATABASE_URL)



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
