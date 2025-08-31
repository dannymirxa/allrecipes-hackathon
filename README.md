# AllRecipes API

## Overview

The AllRecipes API is a robust system for analyzing recipe data, focusing on ingredient co-occurrence and recipe similarity using FastAPI. Designed with efficiency and accuracy in mind, this API leverages pre-computed models and advanced data handling techniques to provide insightful and fast responses.

## Key Features

- **Efficient Ingredient Co-occurrence**: Utilizes pre-computation for swift retrieval of ingredients that frequently appear together.
- **Recipe Similarity Search**: Offers quick and accurate searches through pre-computed TF-IDF matrices.
- **Advanced Data Processing**: Implements robust ingredient normalization and enhanced text processing for meaningful comparisons.

## Technical Details

### Ingredient Co-occurrence

- **Normalization**: Ingredients are standardized via a robust cleaning function that removes numbers, special characters, and common measurement units.
- **Co-occurrence Mapping**: Generates ingredient pairs within recipes to create a co-occurrence map using sets, improving speed and accuracy.
- **Top Co-occurring Ingredients**: Enables rapid lookup and sorting of co-occurring ingredients based on frequency.

### Recipe Similarity Search

- **TF-IDF Vectorization**: Transforms text data of recipes into a TF-IDF matrix for efficient cosine similarity computations.
- **Comprehensive Text Fields**: Combines title, description, and normalized ingredients into a single field to maximize search efficacy.
- **Similarity Computation**: Quickly compares recipes against the pre-computed matrix, returning the top matching recipes.

## Project Structure

```
.
├── models/
│   ├── ingredient_list.py
├── modules/
│   ├── ingredient_cooccurance.py
│   ├── recipes_normalized.py
│   └── recipes_similarity_search.py
├── router/
│   └── ingredients_router.py
├── schemas/
│   └── ingredients.py
├── tests/
│   ├── methods.py
│   └── test_crud.py
├── Dockerfile
├── main.py
├── requirements.txt
└── server.py
```

## Setup Instructions

### Prerequisites

- **Docker**: Ensure Docker is installed. [Get Docker](https://docs.docker.com/get-docker/).

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/dannymirxa/allrecipes-hackathon.git
   cd allrecipes-api
   ```

2. Start the Docker container:
   ```bash
   docker compose up -d
   ```

3. Access the API at `http://localhost:8001`.

## API Endpoints

- **GET /api/ingredient-cooccurrence**: Retrieve top co-occurring ingredients.
  - **Query Parameters**: `ingredient` (string, required).

- **POST /api/recipe-duplicates**: Identify similar recipes.
  - **Payload**: Recipe JSON.

## Testing

Run asynchronous test suites to ensure API functionality.

```bash
# Install testing dependencies
pip install -r requirements.txt

# Run tests
pytest
```

### Testing Tools
- **Httpx**: Utilized for asynchronous requests in testing scenarios.
- **Pydantic**: Used for data validation and handling.

## Design Enhancements and Rationale

- **Pre-computation**: Ensures lookup efficiency and reduces processing overhead in runtime APIs.
- **Vectorization**: Uses combined fields and normalization for enhanced search relevance.

## License

This project is under the MIT License. See `LICENSE` for further details.

## Author

Your Name

## Acknowledgments

Appreciation to contributors and the open-source community for their invaluable tools and software.
