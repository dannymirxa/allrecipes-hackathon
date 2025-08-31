import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from main import app
import json
import pytest
import httpx
import pytest_asyncio
from pydantic import ValidationError
from schemas.ingredients import IngredientCooccurrence, RecipesDuplicates

# use httpx AsyncClient because FastApi TestClient does not work well with Asyncsession

def is_valid_ingredient_cooccurrence(data: dict) -> bool:
    try:
        IngredientCooccurrence.model_validate(data)
        return True
    except ValidationError :
        return False
    
def is_valid_recipe_duplicates(data: dict) -> bool:
    try:
        RecipesDuplicates.model_validate(data)
        return True
    except ValidationError :
        return False

@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(base_url="http://localhost:8001") as client:
        yield client

c
@pytest.mark.asyncio
async def test_get_ingredients_cooccurrence_true(client):
    response = await client.get("/api/ingredient-cooccurrence?ingredient=cinnamon")
    assert response.status_code == 200
    assert is_valid_ingredient_cooccurrence(response.json()) == True

# test get_ingredients_cooccurrence with input with wrong schema
@pytest.mark.asyncio
async def test_get_ingredients_cooccurrence_false_number(client):
    response = await client.get("/api/ingredient-cooccurrence?ingredient=cinnamon123")
    assert response.status_code == 422
    assert is_valid_ingredient_cooccurrence(response.json()) == False
    assert response.json() == {'detail': [{'type': 'string_pattern_mismatch', 'loc': ['query', 'ingredient'], 'msg': "String should match pattern '^[a-zA-Z -]*$'", 'input': 'cinnamon123', 'ctx': {'pattern': '^[a-zA-Z -]*$'}}]}

# test get_ingredients_cooccurrence with non existant input
@pytest.mark.asyncio
async def test_get_ingredients_cooccurrence_false_no_ingredient(client):
    response = await client.get("/api/ingredient-cooccurrence?ingredient=cinnamo")
    assert response.status_code == 500
    assert is_valid_ingredient_cooccurrence(response.json()) == False
    assert response.json() == {'detail': "An unexpected error occurred: 404: Ingredient 'cinnamo' not found or has no co-occurring ingredients."}

# test get_similar_recipes with correct input
@pytest.mark.asyncio
async def test_get_similar_recipes_true(client):
    request_payload = {
        "recipe": {
            "name": "Cinnamon Bun Bread",
            "description": "A moist and delicious cinnamon bun bread that's quick and easy to make.",
            "ingredients": [
                {"name": "all-purpose flour", "quantity": "3 cups"}
            ]
        }
    }
    response = await client.post("/api/recipe-duplicates", json=request_payload)
    assert response.status_code == 200
    assert is_valid_recipe_duplicates(response.json()) == True

@pytest.mark.asyncio
async def test_get_similar_recipes_false_datatype(client):
    request_payload = {
        "recipe": {
            "name": 0,
            "description": "A moist and delicious cinnamon bun bread that's quick and easy to make.",
            "ingredients": [
                {"name": "all-purpose flour", "quantity": "3 cups"}
            ]
        }
    }
    response = await client.post("/api/recipe-duplicates", json=request_payload)
    assert response.status_code == 422
    assert is_valid_recipe_duplicates(response.json()) == False
    assert response.json() == {'detail': [{'type': 'string_type', 'loc': ['body', 'recipe', 'name'], 'msg': 'Input should be a valid string', 'input': 0}]}

@pytest.mark.asyncio
async def test_get_similar_recipes_false_broken_json(client):
    request_payload = """{
        "recipe": {
            "name": "A moist and delicious cinnamon bun bread that's quick and easy to make.",
            "description": "A moist and delicious cinnamon bun bread that's quick and easy to make.",
            "ingredients": [
                {"name": "all-purpose flour", "quantity": "3 cups}
            ]
        }
    }"""
    response = await client.post("/api/recipe-duplicates",
                                 data=request_payload,
                                 headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    assert is_valid_recipe_duplicates(response.json()) == False
    assert response.json() == {'detail': [{'type': 'json_invalid', 'loc': ['body', 314], 'msg': 'JSON decode error', 'input': {}, 'ctx': {'error': 'Invalid control character at'}}]}