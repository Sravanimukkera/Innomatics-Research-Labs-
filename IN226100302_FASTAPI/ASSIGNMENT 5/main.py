from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Task 5 Running"}

@app.get("/hello")
def hello():
    return {"message": "Hello Sravani"}

@app.get("/square/{number}")
def square(number: int):
    return {"number": number, "square": number * number}

class Student(BaseModel):
    name: str
    age: int
    course: str

@app.post("/student")
def create_student(student: Student):
    return {"data": student}

@app.get("/add")
def add(a: int, b: int):
    return {"sum": a + b}