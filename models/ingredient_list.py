from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class ingredientList(base):

    __tablename__ = "ingredient_list"

    id = Column(Integer, primary_key=True, index=True)
    ingredientId = Column(String(40), nullable=True, index=True)
    searchValue = Column(String(20), nullable=True)
    term = Column(String(20), nullable=True)
    useCount = Column(Integer)