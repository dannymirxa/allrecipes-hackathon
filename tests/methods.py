import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import json
from pydantic import ValidationError
from schemas.ingredients import IngredientCooccurrence, RecipesDuplicates

def is_valid_ingredient_cooccurrence(data: dict) -> bool:
    try:
        IngredientCooccurrence.model_validate(data)
        return True
    except ValidationError :
        return False
    
def is_valid_recipe_wrapper(data: dict) -> bool:
    try:
        RecipesDuplicates.model_validate(data)
        return True
    except ValidationError :
        return False

from main import app
import httpx
# use httpx AsyncClient because FastApi TestClient does not work well with Asyncsession

async def create_client():
    return httpx.AsyncClient(base_url="http://localhost:8001")

async def test_get_ingredients_cooccurrence():
    client_instance = await create_client()
    try:
        response = await client_instance.get("/api/ingredient-cooccurrence?ingredient=cinnamon123")
        print(response.status_code)
        print(response.json())
    finally:
        await client_instance.aclose()

import asyncio

# asyncio.run(test_get_ingredients_cooccurrence())

request_payload = {
        "recipe": {
            "name": 0,
            "description": "A moist and delicious cinnamon bun bread that's quick and easy to make.",
            "ingredients": [
                {"name": "all-purpose flour", "quantity": "3 cups"}
            ]
        }}

# request_payload = """{
#         "recipe": {
#             "name": "A moist and delicious cinnamon bun bread that's quick and easy to make.",
#             "description": "A moist and delicious cinnamon bun bread that's quick and easy to make.",
#             "ingredients": [
#                 {"name": "all-purpose flour", "quantity": "3 cups"}
#             ]
#         }
#     }"""

async def test_get_similar_recipes():
    client_instance = await create_client()
    # print(json.loads(request_payload))
    try:
        response = await client_instance.get("/api/recipe-duplicates", 
                                              json=request_payload,
                                                # data=request_payload,
                                                # headers={"Content-Type": "application/json"}
                                              )
        print(response.status_code)
        # print(RecipesDuplicates.model_validate(response.json()))
        print(is_valid_recipe_wrapper(response.json()))
        print(response.json())
        print(response.json() == {'detail': [{'type': 'json_invalid', 'loc': ['body', 314], 'msg': 'JSON decode error', 'input': {}, 'ctx': {'error': 'Invalid control character at'}}]})
    finally:
        await client_instance.aclose()

asyncio.run(test_get_similar_recipes())
