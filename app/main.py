from fastapi import (
    FastAPI, 
    HTTPException, 
    Depends,
    status )
from sqlalchemy.orm import Session

from .provider import search_provider

from . import ( 
    models, 
    schemas, 
    crud )
from .database import (
    SessionLocal, 
    engine )
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/search", status_code=status.HTTP_200_OK)
def search_book(isbn: schemas.Isbn):
    list_isbn = isbn.dict()['isbn']
    search_provider.set_isbn(list_isbn)
    books = search_provider.get_books()
    remove_empty = list(filter(None,books))
    if not remove_empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"ISBN {list_isbn} not found") 
    return remove_empty

@app.get("/books", response_model=List[schemas.Book],status_code=status.HTTP_200_OK)
def get_books(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip,limit=limit)


@app.post("/books", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_books(book: schemas.BookCreate, db: Session = Depends(get_db)):
    created_book = crud.create_book(db=db,book=book)
    if created_book.id:
        for author in book.authors:
            crud.create_author(db=db,author=author,book_id=created_book.id)
        return crud.get_book(db, book_id=created_book.id)


@app.put("/books/{id}")
def modify_books(id):
    pass

@app.delete("/books/{id}")
def modify_books(id):
    pass


@app.get("/comments")
def get_comments():
    pass

@app.post("/comments", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
def get_comments(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db,comment=comment)


@app.delete("/comments/{id_comment}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id_comment: int, db: Session = Depends(get_db)):
    _comment = crud.get_comment(db=db,comment_id = id_comment)
    if _comment:
        return crud.delete_comment(db=db, comment_id=id_comment)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Comment ID {id_comment} not found") 


@app.put("/comments/{id_comment}", status_code=status.HTTP_200_OK)
def modify_comment(comment: schemas.CommentCreate,id_comment: int, db: Session = Depends(get_db)):

    _comment = crud.get_comment(db=db,comment_id = id_comment)
    if _comment:
        return crud.modify_comment(db=db,comment=comment,comment_id=id_comment)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Comment ID {id_comment} not found") 