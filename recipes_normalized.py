import pandas as pd
import json

# Load the corrected JSON file
with open("allrecipes.com_database_12042020000000.json", "r", encoding="utf-8") as f:
    data = json.load(f)


recipes_list = []
categories_list = []
ingredients_list = []
instructions_list = []
nutrition_list = []
reviews_list = []

for recipe in data:
    recipe_id = recipe.get("id")

    # Recipes
    recipes_list.append({
        "id": recipe_id,
        "title": recipe.get("title"),
        "name": recipe.get("name"),
        "description": recipe.get("description"),
        "prep_time": recipe.get("prep_time"),
        "cook_time": recipe.get("cook_time"),
        "total_time": recipe.get("total_time")
    })

    # Categories
    for cat in recipe.get("categories", []):
        categories_list.append({
            "recipe_id": recipe_id,
            "category": cat
        })

    # Ingredients
    for ing in recipe.get("ingredients", []):
        ingredients_list.append({
            "recipe_id": recipe_id,
            "ingredient": ing
        })

    # Instructions
    for step in recipe.get("steps", []):
        instructions_list.append({
            "recipe_id": recipe_id,
            "step_number": step.get("step", None),
            "description": step.get("instruction", None)

        })


    # Nutrition (dictionary)
    nutrition = recipe.get("nutritional_information", {})
    nutrition_list.append({
        "recipe_id": recipe_id,
        "calories": nutrition.get("calories", None),
        "servings": nutrition.get("servings", None),
        "total_fat": nutrition.get("total_fat", None),
        "saturated_fat": nutrition.get("saturated_fat", None),
        "cholesterol": nutrition.get("cholesterol", None),
        "sodium": nutrition.get("sodium", None),
        "potassium": nutrition.get("potassium", None),
        "total_carbohydrate": nutrition.get("total_carbohydrate", None),
        "dietry_fibre": nutrition.get("dietry_fibre", None),
        "protein": nutrition.get("protein", None),
        "sugars": nutrition.get("sugars", None),
        "vitamin_a": nutrition.get("vitamin_a", None),
        "vitamin_c": nutrition.get("vitamin_c", None),
        "calcium": nutrition.get("calcium", None),
        "iron": nutrition.get("iron", None),
        "thiamin": nutrition.get("thiamin", None),
        "niacin": nutrition.get("niacin", None),
        "vitamin_b6": nutrition.get("vitamin_b6", None),
        "magnesium": nutrition.get("magnesium", None),
        "folate": nutrition.get("folate", None)

    })

    # Reviews (list of dicts)
    for review in recipe.get("rating", []):
        reviews_list.append({
            "recipe_id": recipe_id,
            "user_name": review
        })

# Convert to DataFrames
df_recipes = pd.DataFrame(recipes_list)
df_categories = pd.DataFrame(categories_list)
df_ingredients = pd.DataFrame(ingredients_list)
df_instructions = pd.DataFrame(instructions_list)
df_nutrition = pd.DataFrame(nutrition_list)
df_reviews = pd.DataFrame(reviews_list)

# Check shapes
# print("Recipes:", df_recipes.shape)
# print("Categories: ", df_categories.shape)
# print("Ingredients:", df_ingredients.shape)
# print("Instructions:", df_instructions.shape)
# print("Nutrition:", df_nutrition.shape)
# print("Reviews:", df_reviews.shape)

# from settings import app_env_settings_local as settings
# import pandas as pd
# from sqlalchemy import create_engine

# database_url = (
#     f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
#     f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
# )

# engine = create_engine(database_url)

# df_recipes.to_sql('recipes', engine, if_exists='replace', index=False)
# df_categories.to_sql('categories', engine, if_exists='replace', index=False)
# df_ingredients.to_sql('ingredients', engine, if_exists='replace', index=False)
# df_instructions.to_sql('instructions', engine, if_exists='replace', index=False)
# df_nutrition.to_sql('nutrition', engine, if_exists='replace', index=False)
# df_reviews.to_sql('reviews', engine, if_exists='replace', index=False)