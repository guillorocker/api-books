from sqlalchemy import (
    Column, 
    ForeignKey, 
    Integer, 
    String )
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base


class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String, unique=False, index=True)
    id_book = Column(Integer, ForeignKey("books.id"))
    
    book = relationship("Book", back_populates="authors")


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String, unique=False, index=True)
    isbn = Column(String,index=True)
    authors = relationship("Author", back_populates='book')
    comments = relationship("Comment", back_populates='book')
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, 
                        server_default=text('now()'))

class Comment(Base):

    __tablename__ = "comments"

    id = Column(Integer,primary_key=True,index=True)
    comment = Column(String, index=True)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, 
                        server_default=text('now()'))

    id_book = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="comments")
