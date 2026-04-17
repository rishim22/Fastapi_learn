from sqlalchemy import Column, Integer, VARCHAR , String
from base import Base   

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key = True, index = True)
    email = Column(String(255), unique = True, index = True)
    hashed_password = Column(String(255))
    username = Column(String(255), unique = True, index = True) 
    role = Column(String(50), default = "user")
