import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import re
from recipes_normalized import df_ingredients

def top_cooccurring_ingredients(ingredient: str) -> dict:
    # Step 1: Clean ingredient text
    df_ingredients["cleaned_ingredient"] = df_ingredients["ingredient"].str.replace(r"[^a-zA-Z\s-]+", "", regex=True)

    # Step 2: Normalize by removing units and stopwords
    units_stopwords = r"\b(cup|cups|tablespoon|tablespoons|teaspoon|teaspoons|ounce|ounces|package|fluid|pound|pounds|slice|slices|or|as|needed|and|to|taste)\b"
    df_ingredients["norm_ingredient"] = df_ingredients["cleaned_ingredient"].str.replace(units_stopwords, "", flags=re.IGNORECASE, regex=True).str.strip()

    # Step 3: Identify recipes that contain 'cinnamon'
    cinnamon_recipes = df_ingredients[df_ingredients["norm_ingredient"].str.contains(ingredient, case=False, na=False)]["recipe_id"].unique()

    # Step 4: Filter ingredients from those recipes, excluding 'cinnamon'
    cooccurring = df_ingredients[
        (df_ingredients["recipe_id"].isin(cinnamon_recipes)) &
        (~df_ingredients["norm_ingredient"].str.contains(ingredient, case=False, na=False))
    ]

    # Step 5: Count co-occurring ingredients
    top_cooccurrence = cooccurring["norm_ingredient"].value_counts().head(10).reset_index()
    top_cooccurrence.columns = ["ingredient", "count"]

    result_dict = {
        "ingredient": ingredient,
        "cooccurrence": top_cooccurrence.to_dict(orient="records")
    }

    return result_dict

# Display result
# print(top_cooccurring_ingredients("cinnamon"))