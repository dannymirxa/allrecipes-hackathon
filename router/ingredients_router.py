# ingredients.py (in api/ folder)

from fastapi import APIRouter, HTTPException, Query, status, Request
from schemas.ingredients import (
    IngredientCooccurrence,
    RecipesDuplicates,
    RecipeWrapper
)
# Import the lookup functions, not the processing functions
from modules.ingredient_cooccurance_count import get_top_cooccurring
from modules.recipe_similarity_search import RecipeSimilarityModel

router = APIRouter(prefix="/api")

@router.get(
    "/ingredient-cooccurrence",
    response_model=IngredientCooccurrence,
    summary="Get Top Co-occurring Ingredients"
)
async def get_ingredients_cooccurrence(
    request: Request,
    ingredient: str = Query(
        ...,
        min_length=2,
        max_length=50,
        regex="^[a-zA-Z -]*$",
        description="The ingredient to find co-occurrences for."
    )
):
    """
    Provides a top 10 list of ingredients commonly used with a specified ingredient.
    """
    try:
        # Access the pre-computed map from the application state
        cooccurrence_map = request.app.state.cooccurrence_map
        
        # The lookup function is now very fast
        result_dict = get_top_cooccurring(ingredient, cooccurrence_map)
        
        # Handle the edge case where the ingredient is not found
        if not result_dict["cooccurrence"]:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ingredient '{ingredient}' not found or has no co-occurring ingredients."
            )
            
        return IngredientCooccurrence.model_validate(result_dict)
    
    except Exception as e:
        # Generic error handler for any unexpected issues
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )

@router.post(
    "/recipe-duplicates",
    response_model=RecipesDuplicates,
    summary="Find Similar Recipes"
)
async def get_similar_recipes(request: Request, recipe: RecipeWrapper):
    """
    Accepts a recipe payload and returns a top 5 list of similar recipes
    from the database.
    """
    try:
        # Access the pre-initialized model from the application state
        similarity_model: RecipeSimilarityModel = request.app.state.similarity_model
        
        # The find_similar_recipes method is now very fast
        similar_recipes = similarity_model.find_similar_recipes(recipe)
        
        return RecipesDuplicates.model_validate(similar_recipes)
        
    except Exception as e:
        # Generic error handler
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )