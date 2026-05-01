from fastapi import FastAPI,Depends,status,HTTPException
import model
from database1 import engine,get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel


app=FastAPI()

class BookStore(BaseModel):
    id:int
    title:str
    author:str
    publish_year:int


class UpdateBook(BaseModel):
    title: str
    author: str
    publish_year: str

@app.post('/book')
def create_book(books:BookStore,db:Session=Depends(get_db)):
    new_book=model.Book(id=books.id,title=books.title,author=books.author,publish_year=books.publish_year)
    db.add(new_book)
    db.commit()
    db.refresh()
    return new_book


@app.get('/book')
def get_book(db:Session=Depends(get_db)):
    books=db.query(model.Book).all()
    return books


@app.put('/book/{book_id}')
def update_book(book_update:UpdateBook,book_id:int,db:Session=Depends(get_db)):
    books=db.query(model.Book).filter(model.Book.id==book_id).first()
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    books.title=book_update.title
    books.author=book_update.author
    books.publish_year=book_update.publish_year

    db.commit()
    db.refresh(books)
    return books



@app.delete('/book/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(book_id:int,db:Session=Depends(get_db)):
    books=db.query(model.Book).filter(model.Book.id==book_id).first()
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    db.delete(books)
    db.commit()

    return {'message':'deleted successfuly'}



    
