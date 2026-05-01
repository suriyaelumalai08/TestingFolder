from fastapi import FastAPI,status,HTTPException 
from typing import Optional
from pydantic import BaseModel


my_books=[
    {
        'id':1,
        'bookname':'python',
        'author':'suriya'
    },
     {
        'id':2,
        'bookname':'c',
        'author':'suriya'
    },
     {
        'id':3,
        'bookname':'java',
        'author':'anif'
    },
]


app=FastAPI()

@app.get('/')
def root():
    return {'message':'hello worl'}

@app.get('/second')
def root2():
    return {'message':'hello & this is root2'}

@app.get("/one/")
def root3(name:str,age:Optional[int]=None):
    return {'message':f'{name} skjl {age}'}


class Student(BaseModel):
    name:str
    age:int
    roll:str

@app.post('/create')
def create(student:Student):
    return {
        'name':student.name,
        'age':student.age,
        'roll':student.roll
    }


@app.get('/book')
def books():
    return my_books

class BOOKS(BaseModel):
    id:int
    bookname:str
    author:str


@app.post('/book')
def books(books:BOOKS):
    new_book=books.model_dump()
    my_books.append(new_book)

@app.get('/find/{bood_id}')
def get_book(book_id:int):
    for book in my_books:
        if book['id']==book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='book not found')

class update_book(BaseModel):
    bookname1:str
    author1:str


@app.put('/update/{book_id}')
def bookupdate(book_id:int,book1:update_book):
    for book in my_books:
        if book['id']==book_id:
            book['bookname']=book1.bookname1
            book['author']=book1.author1
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='book not found')

@app.delete('/delete/{book_id}')
def delete_book(book_id:int):
    for book in my_books:
        if book['id']==book_id:
            my_books.remove(book)
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='book not found')
    
