from fastapi import FastAPI
from contextlib import asynccontextmanager

from modules.ingredient_cooccurance import precompute_cooccurrences
from modules.recipes_similarity_search import RecipeSimilarityModel
from modules.recipes_normalized import load_and_normalize_data

from router.ingredients_router import router

# this is needed to initialize the heavy resources ONCE
@asynccontextmanager
async def lifespan(app: FastAPI):
    # load and normalize the raw data once
    all_dataframes = load_and_normalize_data("allrecipes.com_database_12042020000000.json")
    df_recipes = all_dataframes["recipes"]
    df_ingredients = all_dataframes["ingredients"]
    
    # compute the co-occurrence map once
    app.state.cooccurrence_map = precompute_cooccurrences(df_ingredients)
    
    # initialize the similarity model once
    app.state.similarity_model = RecipeSimilarityModel(df_recipes, df_ingredients)
    
    yield

# initialize the FastAPI app with the lifespan manager
app = FastAPI(
    title="AllRecipes API",
    description="API for recipe ingredient co-occurrence and similarity search.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)