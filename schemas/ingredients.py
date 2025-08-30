from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from typing import List

class Cooccurrence(BaseModel):
    ingredient: str
    count: int

class IngredientCooccurrence(BaseModel):
    ingredient: str
    cooccurrence: List[Cooccurrence]

class Duplicate(BaseModel):
    name: str
    similarity: float

class RecipesDuplicates(BaseModel):
    duplicates: List[Duplicate]

class Ingredient(BaseModel):
    name: str
    quantity: str

class Recipe(BaseModel):
    name: str
    description: str
    ingredients: List[Ingredient]

class RecipeWrapper(BaseModel):
    recipe: Recipe

class ErrorMessage(BaseModel):
    error: str