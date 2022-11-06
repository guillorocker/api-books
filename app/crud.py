from sqlalchemy.orm import Session
from . import (
    models, 
    schemas )



def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    book_dict = book.dict()
    book_dict.pop('authors')
    db_item = models.Book(**book_dict)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    print(db_item)
    return db_item

def create_author(db: Session, author: str, book_id: int):
    db_item = models.Author(**{'name':author,'id_book':book_id})
    db.add(db_item)
    db.commit()
    return True


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def get_comment_by_book(db: Session, book_id: int, skip: int=0, limit: int= 100):
    return db.query(models.Comment).filter(models.Comment.id_book == book_id).all()

def create_comment(db: Session, comment: schemas.CommentCreate):
    print(comment.dict())
    db_item = models.Comment(**comment.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_comment(db: Session, comment_id: int):
    db.query(models.Comment).filter(models.Comment.id == comment_id).delete()
    db.commit()
    return True
  

def modify_comment(db: Session, comment: schemas.CommentCreate, comment_id: int):
    db.query(models.Comment).filter(models.Comment.id == comment_id).update(comment.dict())
    db.commit()
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()
