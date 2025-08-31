import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

from schemas.ingredients import RecipeWrapper
from modules.recipes_normalized import load_and_normalize_data

def normalize_ingredient_name(ingredient: str) -> str:
    # cleans and normalizes a raw ingredient string.
    text = ingredient.lower()
    text = re.sub(r"[^a-z\s-]", "", text)
    units_stopwords = r"\b(cup|cups|c|tablespoon|tablespoons|tbsp|teaspoon|teaspoons|tsp|ounce|ounces|oz|package|pkg|fluid|fl|pound|pounds|lb|slice|slices|or|as|needed|and|to|taste|chopped|diced|minced|sliced)\b"
    text = re.sub(units_stopwords, "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text

class RecipeSimilarityModel:
    def __init__(self, df_recipes: pd.DataFrame, df_ingredients: pd.DataFrame):
        self.df_recipes = df_recipes
        self.df_ingredients = df_ingredients
        
        self._prepare_data()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self._fit_vectorizer()

    def _prepare_data(self):
        # processes the recipe data to create a combined text field for TF-IDF.
        # includes normalizing ingredients and combining title, description, and ingredients.

        # normalize ingredients for all recipes
        self.df_ingredients['norm_ingredient'] = self.df_ingredients['ingredient'].apply(normalize_ingredient_name)
        
        # group normalized ingredients by recipe
        # example. recipe_id: 100008, norm_ingredient: "fresh young ginger root peeled sea salt rice vinegar white sugar"
        ingredients_grouped = self.df_ingredients.groupby('recipe_id')['norm_ingredient'].apply(lambda x: ', '.join(x))
        
        # merge ingredients back into the main recipes dataframe
        self.df_recipes = self.df_recipes.merge(ingredients_grouped, left_on='id', right_index=True, how='left')
        
        # create a single text field with all relevant info (title, description, ingredients)
        # title removed because the title in example input uses description
        self.df_recipes['combined_text'] = (
            self.df_recipes['title'].fillna('') + ': ' +
            self.df_recipes['description'].fillna('') + '; ' +
            self.df_recipes['norm_ingredient'].fillna('')
        )
    
    def _fit_vectorizer(self):

        # train the vectorizer on the entire dataset's combined text
        return self.vectorizer.fit_transform(self.df_recipes['combined_text'])

    def find_similar_recipes(self, input_recipe: RecipeWrapper, top_n: int = 5) -> dict:
        # finds the top N most similar recipes for a given input recipe.

        # 1. prepare the input recipe's text using the same normalization
        input_ingredients = ', '.join([normalize_ingredient_name(ing.name) for ing in input_recipe.recipe.ingredients])
        input_text = (
            input_recipe.recipe.name + ': ' +
            input_recipe.recipe.description + '; ' +
            input_ingredients
        )
        
        # 2. transform the input text using the trained vectorizer
        input_vector = self.vectorizer.transform([input_text])
        
        # 3. compute cosine similarity against the pre-computed matrix
        cosine_sim = cosine_similarity(input_vector, self.tfidf_matrix).flatten()
        
        # 4. get the top N matches
        # sort the indices of the similarity scores in descending order
        top_indices = cosine_sim.argsort()[-top_n:][::-1]
        
        duplicates = [{
            "name": self.df_recipes.iloc[i]['title'],
            "similarity": round(float(cosine_sim[i]), 2)
        } for i in top_indices]
        
        return {"duplicates": duplicates}

# test the logic below:

# if __name__ == "__main__":

#     all_dataframes = load_and_normalize_data("allrecipes.com_database_12042020000000.json")
#     df_recipes = all_dataframes["recipes"]
#     df_ingredients = all_dataframes["ingredients"]

#     similarity_model = RecipeSimilarityModel(df_recipes, df_ingredients)

#     input_recipe_data = {
#         "recipe": {
#             "name": "Cinnamon Bun Bread",
#             "description": "A moist and delicious cinnamon bun bread that's quick and easy to make.",
#             "ingredients": [
#                 {"name": "all-purpose flour", "quantity": "3 cups"},
#                 {"name": "baking powder", "quantity": "1 tablespoon"},
#                 {"name": "salt", "quantity": "1/4 teaspoon"},
#                 {"name": "white sugar", "quantity": "1 cup"},
#                 {"name": "milk", "quantity": "1 1/2 cups"},
#                 {"name": "egg", "quantity": "1"},
#                 {"name": "vegetable oil", "quantity": "1/3 cup"},
#                 {"name": "vanilla extract", "quantity": "2 teaspoons"},
#                 {"name": "brown sugar", "quantity": "1 cup"},
#                 {"name": "ground cinnamon", "quantity": "2 tablespoons"},
#                 {"name": "butter", "quantity": "1/2 cup"}
#             ]
#         }
#     }

#     input_recipe = RecipeWrapper.model_validate(input_recipe_data)

#     result = similarity_model.find_similar_recipes(input_recipe)
    
#     import json
#     print(json.dumps(result, indent=2))