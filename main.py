from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel  
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}   

@app.get("/greet")
def greet():
    return {"message": "Hello, paglu!"}

@app.get("/greet/{name}")
def greet_name(name: str,age: int,gender: Optional[str] = None):
    return {"message": f"Hello, {name}! and you are {age} years old. while your gender is {gender}"}
 
class Student(BaseModel):
    name: str
    age: int
    roll_no: int

@app.post("/create_Student")
def create_student(student: Student):
    return {"message": f"Student {student.name} created successfully with age {student.age} and roll number {student.roll_no}"}