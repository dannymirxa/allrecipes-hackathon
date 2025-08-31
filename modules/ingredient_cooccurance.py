import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
from collections import defaultdict
from itertools import combinations
import pandas as pd
from modules.recipes_normalized import load_and_normalize_data

def normalize_ingredient_name(ingredient: str) -> str:
    # remove lowercase and remove numbers and special characters
    text = ingredient.lower()
    text = re.sub(r"[^a-z\s-]", "", text)

    # remove measurement units
    units_stopwords = r"\b(cup|cups|c|tablespoon|tablespoons|tbsp|teaspoon|teaspoons|tsp|ounce|ounces|oz|package|pkg|fluid|fl|pound|pounds|lb|slice|slices|or|as|needed|and|to|taste|chopped|diced|minced|sliced)\b"
    text = re.sub(units_stopwords, "", text, flags=re.IGNORECASE)
    
    # trim spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

def precompute_cooccurrences(df_ingredients: pd.DataFrame) -> defaultdict:
    
    # clean up the ingredients and remove null/ empty string
    df_ingredients["norm_ingredient"] = df_ingredients["ingredient"].apply(normalize_ingredient_name)
    df_ingredients.dropna(subset=["norm_ingredient"], inplace=True)
    df_ingredients = df_ingredients[df_ingredients["norm_ingredient"] != ""]
    
    # group ingredients by recipe and get a unique set for the ingredients
    # example. receipe_id: 10003, norm_ingredient: {'confectioners sugar', 'cornstarch', 'vanilla extract', 'butter', 'all-purpose flour'}
    recipe_ingredients = df_ingredients.groupby("recipe_id")["norm_ingredient"].apply(set)

    # auto initialize default value for key not yet exist
    co_occurrence_map = defaultdict(lambda: defaultdict(int))
    for ingredients_set in recipe_ingredients:
        # create unique pairs of 2 of ingredients for the recipe
        for ing1, ing2 in combinations(ingredients_set, 2):
            co_occurrence_map[ing1][ing2] += 1
            co_occurrence_map[ing2][ing1] += 1
    
    return co_occurrence_map

def get_top_cooccurring(ingredient: str, cooccurrence_map: defaultdict) -> dict:

    normalized_ingredient = normalize_ingredient_name(ingredient)
    
    if normalized_ingredient not in cooccurrence_map:
        return {"ingredient": ingredient, "cooccurrence": []}

    # sort co-occurring ingredients by count
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

# inspect the logic below:

# if __name__ == "__main__":
#     all_dataframes = load_and_normalize_data("allrecipes.com_database_12042020000000.json")
#     df_ingredients = all_dataframes["ingredients"]
        
#     import json
#     # compute the co-occurrence map
#     CO_OCCURRENCE_MAP = precompute_cooccurrences(df_ingredients)
    
#     print(json.dumps(CO_OCCURRENCE_MAP, indent=2))

#     # testing the function
#     result = get_top_cooccurring("cinnamon", CO_OCCURRENCE_MAP)

#     print(json.dumps(result, indent=2))