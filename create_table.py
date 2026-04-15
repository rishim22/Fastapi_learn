from database import engine, Base
import model
from model import Book
 
Base.metadata.create_all(bind=engine)
