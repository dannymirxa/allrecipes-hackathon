from settings import app_env_settings_local as settings
import asyncio
from database_setup import  database_url, database  # Import from new setup file
from models.ingredient_list import ingredientList  # Import your model
import pandas as pd
from sqlalchemy import create_engine

database_url = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_engine(database_url)
inngredient_data = pd.read_json('data.json')
inngredient_data.to_sql('ingredient_list', engine, if_exists='replace')