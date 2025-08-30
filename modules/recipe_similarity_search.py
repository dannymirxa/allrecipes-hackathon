import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


from schemas.ingredients import RecipeWrapper
from recipes_normalized import df_recipes, df_ingredients

def find_similar_recipes(input_recipe: RecipeWrapper, df_recipes: pd.DataFrame, df_ingredients: pd.DataFrame, top_n=5):
    # Combine title and ingredients for each recipe
    df_combined = df_recipes.copy()
    ingredients_grouped = df_ingredients.groupby('recipe_id')['ingredient'].apply(lambda x: ', '.join(x))
    df_combined = df_combined.merge(ingredients_grouped, left_on='id', right_index=True, how='left')
    df_combined['combined_text'] = df_combined['title'].fillna('') + ': ' + df_combined['ingredient'].fillna('')
    
    # Prepare input recipe text
    input_text = input_recipe.recipe.name + ', ' + ' '.join([f"{ing.quantity} {ing.name}, " for ing in input_recipe.recipe.ingredients])
    
    # Vectorize
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(df_combined['combined_text'].tolist() + [input_text])
    
    # Compute similarity
    cosine_sim = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
    
    # Get top matches
    top_indices = cosine_sim.argsort()[-top_n:][::-1]
    duplicates = [{"name": df_combined.iloc[i]['title'], "similarity": round(float(cosine_sim[i]), 2)} for i in top_indices]
    
    return {"duplicates": duplicates}

# input_recipe = {
#                 "recipe": {
#                     "name": "Cinnamon Bun Bread",
#                     "description": "A moist and delicious cinnamon bun bread that's quick and easy to make.",
#                     "ingredients": [
#                         {"name": "all-purpose flour", "quantity": "3 cups"},
#                         {"name": "baking powder", "quantity": "1 tablespoon"},
#                         {"name": "salt", "quantity": "1/4 teaspoon"},
#                         {"name": "white sugar", "quantity": "1 cup"},
#                         {"name": "milk", "quantity": "1 1/2 cups"},
#                         {"name": "egg", "quantity": "1"},
#                         {"name": "vegetable oil", "quantity": "1/3 cup"},
#                         {"name": "vanilla extract", "quantity": "2 teaspoons"},
#                         {"name": "brown sugar", "quantity": "1 cup"},
#                         {"name": "ground cinnamon", "quantity": "2 tablespoons"},
#                         {"name": "butter", "quantity": "1/2 cup"}
#                     ]
#                     }
#                 }

# from schemas.ingredients import (
#     IngredientCooccurrence,
#     RecipesDuplicates,
#     Recipe,
#     RecipeWrapper
# )
# print(RecipeWrapper.model_validate(input_recipe))
# result = find_similar_recipes(input_recipe, df_recipes, df_ingredients)
# print(RecipesDuplicates.model_validate({'duplicates': [{'name': 'Cinnamon Swirl Bread', 'similarity': 0.66}, {'name': 'Cinnamon Bread I', 'similarity': 0.65}, {'name': 'Cinnamon Sugar Cookies', 'similarity': 0.64}, {'name': 'Cinnamon Lemon Cookies', 'similarity': 0.63}, {'name': 'Easy Apple Cinnamon Muffins', 'similarity': 0.63}]}))
# print(result)