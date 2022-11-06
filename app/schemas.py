from datetime import datetime
from pydantic import BaseModel
from typing import List


class Isbn(BaseModel):
    isbn: List


class CommentsBase(BaseModel):
    id_book: int
    comment: str
    created_at: datetime = None


class CommentCreate(BaseModel):
    comment: str
    id_book: int

class Comment(CommentsBase):
    comment: str


    class Config:
        orm_mode = True



class AuthorBase(BaseModel):
    name: str


class AuthorCreate(BaseModel):
    name: str
    id_book: int


class Author(AuthorBase):
    name: str

    class Config:
        orm_mode = True





class BookBase(BaseModel):
    id: int
    isbn : str
    title: str     
    authors: List[Author] = None
    comments: List[Comment] = None   


class BookCreate(BaseModel):
    isbn: str
    title: str
    authors: List[str]
    

class Book(BookBase):
    created_at: datetime = None

    class Config:
        orm_mode = True
