import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import APIRouter, HTTPException, Query, status

from modules.ingredient_cooccurance_count import top_cooccurring_ingredients
from modules.recipe_similarity_search import find_similar_recipes
from recipes_normalized import df_recipes, df_ingredients

from schemas.ingredients import (
    IngredientCooccurrence,
    RecipesDuplicates,
    RecipeWrapper
)

router = APIRouter(prefix="/api")

@router.get("/ingredient-cooccurrence", response_model=IngredientCooccurrence)
async def get_ingredients_cooccurance(
    ingredient: str = Query(..., min_length=1, max_length=50,
                            regex="^[a-zA-Z ]*$",
                            description="The ingredient to find co-occurrences for")):
    try:
        cooccuring_ingredients = top_cooccurring_ingredients(ingredient)
        result = IngredientCooccurrence.model_validate(cooccuring_ingredients)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")


@router.post("/recipe-duplicates", response_model=RecipesDuplicates)
async def get_similar_recipes(recipe: RecipeWrapper):
    try:
        if not isinstance(recipe, RecipeWrapper):
            raise ValueError("Invalid input for RecipeWrapper")
        similar_recipes = find_similar_recipes(recipe, df_recipes, df_ingredients)
        result = RecipesDuplicates.model_validate(similar_recipes)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")
    