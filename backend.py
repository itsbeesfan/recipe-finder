from fastapi import FastAPI, Query
import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
from typing import Optional

# Initialize the FastAPI app
app = FastAPI()

# Spoonacular API credentials
SPOONACULAR_API_KEY = os.getenv("8e393dc9acab4bb8bfaccfec8a351341", "8e393dc9acab4bb8bfaccfec8a351341")  # Replace with your API key
SPOONACULAR_BASE_URL = "https://api.spoonacular.com"

@app.get("/recipes/complexSearch")
async def complex_search(
        includeIngredients: str,
        minCalories: Optional[int] = None,
        minProtein: Optional[int] = None,
        maxCalories: Optional[int] = None,
        maxCarbs: Optional[int] = None,
        number: int = 5
):
    # Clean the ingredients parameter to handle any extra spaces or formatting issues
    includeIngredients_cleaned = includeIngredients.replace(", ", ",").strip()

    # Construct the API URL
    api_url = f"{SPOONACULAR_BASE_URL}/recipes/complexSearch"

    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "includeIngredients": includeIngredients_cleaned,
        "minCalories": minCalories,
        "minProtein": minProtein,
        "maxCalories": maxCalories,
        "maxCarbs": maxCarbs,
        "number": number,
    }

    # Make the external API request
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        logging.error("Unauthorized: Check your API key.")
        return {"error": "Unauthorized. Please check the API key."}
    else:
        logging.error(f"Failed to fetch recipes: {response.status_code}")
        return {"error": f"Failed to fetch recipes: {response.status_code}"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
