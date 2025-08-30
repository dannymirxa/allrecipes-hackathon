WITH ingredients_cleaned as (
SELECT
    recipe_id,
    regexp_replace(ingredient, '[^a-zA-Z\s]+', '', 'g') AS cleaned_ingredient
FROM
    ingredients),
normalized as(
SELECT recipe_id,
    trim(regexp_replace(
        cleaned_ingredient, 
        '\m(cup|cups|tablespoon|tablespoons|teaspoon|teaspoons|ounce|ounces|package|fluid|pound|pounds|slice|slices|or|as|needed|and|to|taste)\M', 
        '', 
        'ig'
    )) as norm_ingredient
FROM ingredients_cleaned
),
target_recipes AS (
    SELECT recipe_id
    FROM normalized
    WHERE norm_ingredient ILIKE '%cinnamon%'
),
cooccurrence AS (
    SELECT n2.norm_ingredient AS ingredient, COUNT(*) AS count
    FROM normalized n2
    JOIN target_recipes tr ON n2.recipe_id = tr.recipe_id
    WHERE n2.norm_ingredient NOT ILIKE '%cinnamon%'
    GROUP BY n2.norm_ingredient
)
SELECT ingredient, count
FROM cooccurrence
ORDER BY count DESC
LIMIT 10;
;