import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
from collections import defaultdict
from itertools import combinations
import pandas as pd
from modules.recipes_normalized import load_and_normalize_data

def normalize_ingredient_name(ingredient: str) -> str:
    # Lowercase and remove non-alpha characters
    text = ingredient.lower()
    text = re.sub(r"[^a-z\s-]", "", text)

    # Remove common units and stopwords
    units_stopwords = r"\b(cup|cups|c|tablespoon|tablespoons|tbsp|teaspoon|teaspoons|tsp|ounce|ounces|oz|package|pkg|fluid|fl|pound|pounds|lb|slice|slices|or|as|needed|and|to|taste|chopped|diced|minced|sliced)\b"
    text = re.sub(units_stopwords, "", text, flags=re.IGNORECASE)
    
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

def precompute_cooccurrences(df_ingredients: pd.DataFrame) -> defaultdict:
    """
    Pre-computes the co-occurrence map for all ingredients.
    """
    df_ingredients["norm_ingredient"] = df_ingredients["ingredient"].apply(normalize_ingredient_name)
    df_ingredients.dropna(subset=["norm_ingredient"], inplace=True)
    df_ingredients = df_ingredients[df_ingredients["norm_ingredient"] != ""]
    
    # Group ingredients by recipe and get a unique set for each
    recipe_ingredients = df_ingredients.groupby("recipe_id")["norm_ingredient"].apply(set)

    co_occurrence_map = defaultdict(lambda: defaultdict(int))
    for ingredients_set in recipe_ingredients:
        # Generate all unique pairs of ingredients for the recipe
        for ing1, ing2 in combinations(ingredients_set, 2):
            co_occurrence_map[ing1][ing2] += 1
            co_occurrence_map[ing2][ing1] += 1
    
    return co_occurrence_map

def get_top_cooccurring(ingredient: str, cooccurrence_map: defaultdict) -> dict:
    """
    Performs a fast lookup to get top 10 co-occurring ingredients.
    """
    normalized_ingredient = normalize_ingredient_name(ingredient)
    
    if normalized_ingredient not in cooccurrence_map:
        return {"ingredient": ingredient, "cooccurrence": []}

    # Sort co-occurring ingredients by count
    top_cooccurring = sorted(
        cooccurrence_map[normalized_ingredient].items(),
        key=lambda item: item[1],
        reverse=True
    )[:10]

    return {
        "ingredient": ingredient,
        "cooccurrence": [
            {"ingredient": ing, "count": count} for ing, count in top_cooccurring
        ]
    }

def top_cooccurring_ingredients(ingredient: str, df_ingredients: pd.DataFrame) -> dict:
    # Pre-compute the co-occurrence map (Heavy, one-time operation)
    CO_OCCURRENCE_MAP = precompute_cooccurrences(df_ingredients)

    # Perform a fast lookup (This is what the API endpoint would do)
    result = get_top_cooccurring(ingredient, CO_OCCURRENCE_MAP)

    return result

# if __name__ == "__main__":
#     # 1. Load and normalize the raw data from the JSON file
#     #    (This would be the first step in your data pipeline)
#     all_dataframes = load_and_normalize_data("allrecipes.com_database_12042020000000.json")
#     df_ingredients = all_dataframes["ingredients"]

#     # 2. Pre-compute the co-occurrence map (Heavy, one-time operation)
#     #    In a real application, this map would be saved and loaded by the API server on startup.
#     CO_OCCURRENCE_MAP = precompute_cooccurrences(df_ingredients)

#     # 3. Perform a fast lookup (This is what the API endpoint would do)
#     result = get_top_cooccurring("cinnamon", CO_OCCURRENCE_MAP)
    
#     import json
#     print("\n--- API Result for 'cinnamon' ---")
#     print(json.dumps(result, indent=2))