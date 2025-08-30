import json
from typing import Dict, List
import pandas as pd

def load_and_normalize_data(file_path: str) -> Dict[str, pd.DataFrame]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Prepare lists to hold normalized data
    recipes_list: List[Dict] = []
    categories_list: List[Dict] = []
    ingredients_list: List[Dict] = []
    instructions_list: List[Dict] = []
    nutrition_list: List[Dict] = []

    for recipe in data:
        recipe_id = recipe.get("id")

        # Main recipe details
        recipes_list.append({
            "id": recipe_id,
            "title": recipe.get("title"),
            "description": recipe.get("description"),
            "prep_time": recipe.get("prep_time"),
            "cook_time": recipe.get("cook_time"),
            "total_time": recipe.get("total_time"),
        })

        # Categories (one-to-many)
        for cat in recipe.get("categories", []):
            categories_list.append({"recipe_id": recipe_id, "category": cat})

        # Ingredients (one-to-many)
        for ing in recipe.get("ingredients", []):
            ingredients_list.append({"recipe_id": recipe_id, "ingredient": ing})

        # Instructions (one-to-many)
        for step in recipe.get("steps", []):
            instructions_list.append({
                "recipe_id": recipe_id,
                "step_number": step.get("step"),
                "description": step.get("instruction"),
            })

        # Nutrition (one-to-one)
        nutrition = recipe.get("nutritional_information", {})
        nutrition_info = {
            key: nutrition.get(key) for key in [
                "calories", "servings", "total_fat", "saturated_fat", "cholesterol",
                "sodium", "potassium", "total_carbohydrate", "dietry_fibre", "protein",
                "sugars", "vitamin_a", "vitamin_c", "calcium", "iron", "thiamin",
                "niacin", "vitamin_b6", "magnesium", "folate"
            ]
        }
        nutrition_info["recipe_id"] = recipe_id
        nutrition_list.append(nutrition_info)

    # Convert lists to DataFrames
    dataframes = {
        "recipes": pd.DataFrame(recipes_list),
        "categories": pd.DataFrame(categories_list),
        "ingredients": pd.DataFrame(ingredients_list),
        "instructions": pd.DataFrame(instructions_list),
        "nutrition": pd.DataFrame(nutrition_list),
    }

    return dataframes

# print(load_and_normalize_data('allrecipes.com_database_12042020000000.json')['recipes'])
# print(load_and_normalize_data('allrecipes.com_database_12042020000000.json')['categories'])
# print(load_and_normalize_data('allrecipes.com_database_12042020000000.json')['ingredients'])
# print(load_and_normalize_data('allrecipes.com_database_12042020000000.json')['instructions'])
# print(load_and_normalize_data('allrecipes.com_database_12042020000000.json')['nutrition'])