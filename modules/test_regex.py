import re
from rapidfuzz import process

recipe_ingredients = [
    "2 cups all-purpose flour",
    "2 tablespoons white sugar",
    "3 teaspoons baking powder",
    "1/2 teaspoon salt",
    "1/2 cup butter, chilled",
    "1 egg",
    "1/2 cup cold milk",
    "1/4 cup raspberry jam"
]

data_json_ingredients = [
    "all-purpose flour", "white sugar", "baking powder", "salt", "butter", "egg", "milk", "raspberry jam"
]

# Clean and extract ingredient names
def clean_ingredient(text):
    return re.sub(r'^[\d/]+\s*\w*\s*', '', text).lower().strip()

cleaned_recipe = [clean_ingredient(item) for item in recipe_ingredients]

# Fuzzy match
matches = {}
for item in cleaned_recipe:
    match, score, _ = process.extractOne(item, data_json_ingredients)
    matches[item] = match if score > 80 else None

print(matches)