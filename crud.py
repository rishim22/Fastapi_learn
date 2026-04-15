from fastapi import FastAPI,status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

books = [
    {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho"},
    {"id": 2, "title": "The God of small things", "author": "Arundhati Roy"},
    {"id": 3, "title": "The White Tiger", "author": "Aravind Adiga"},
    {"id": 4, "title": "The Palace of illusions", "author": "Chitra Banerjee Divakaruni"},
]

app = FastAPI()

@app.get("/books")
def get_books():
    return books   

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"]== book_id:
            return book
    """return {"message": "Book not found"}"""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

class Book(BaseModel):
    id: int
    title: str  
    author: str

@app.post("/book")
def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book

class UpdateBook(BaseModel):
    id: int
    title: str  
    author: str
 
@app.put("/book/{book_id}")
def update_book(book_id: int, updated_book: UpdateBook):
   for book in books:
        if book["id"] == book_id:
            book["title"] = updated_book.title
            book["author"] = updated_book.author
            return book
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found to update")
   
@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found to delete")