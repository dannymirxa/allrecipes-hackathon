# AllRecipes Hackathon Project

## Project Overview

This project processes and analyzes recipe data with functionalities for finding top co-occurring ingredients and searching for similar recipes using FastAPI. It integrates operations on datasets to understand relationships between ingredients and to provide recipe suggestions based on similarity.

## Setup Instructions

### Prerequisites

- Python 3.x
- Libraries: `pandas`, `scikit-learn`, `FastAPI`, `Uvicorn`, `re` for regular expressions

### Installation

1. Clone the repository:
   ```bash
   git clone https://path-to-repo.git
   cd allrecipes-hackathon
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

Start the server using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at `http://localhost:8000`.

## API Documentation

### Endpoints

#### **Ingredient Co-occurrence**

- **URL:** `/api/ingredient-cooccurrence`
- **Method:** `GET`
- **Query Parameter:** `ingredient` (string, required, 2-50 characters, alphabetic, spaces, and hyphens allowed)

Description: Retrieves the top 10 co-occurring ingredients for a specified ingredient by analyzing available recipes. It utilizes a pre-computed map for fast access.

Example:
```bash
curl -X 'GET' 'http://localhost:8000/api/ingredient-cooccurrence?ingredient=cinnamon'
```

#### **Recipe Duplicates**

- **URL:** `/api/recipe-duplicates`
- **Method:** `POST`
- **Request Body:** JSON object conforming to `RecipeWrapper` schema

Description: Finds and returns a list of up to 5 recipes with the highest similarity scores to the provided recipe using cosine similarity on TF-IDF vectors.

Example:
```bash
curl -X 'POST' 'http://localhost:8000/api/recipe-duplicates' \
-H 'Content-Type: application/json' \
-d '{
    "recipe": {
        "name": "Cinnamon Bun Bread",
        "ingredients": [
            {"name": "all-purpose flour", "quantity": "3 cups"},
            {"name": "baking powder", "quantity": "1 tablespoon"},
            ...
        ]
    }
}'
```

## Contributors

- [Contributor Names]

## License

This project is licensed under the MIT License.