import requests
from bs4 import BeautifulSoup
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_recipe(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title_tag = soup.find("span", class_="o-AssetTitle__a-HeadlineText")
        title = title_tag.text.strip() if title_tag else "Title not found"
        
        # Extract ingredients
        ingredients_section = soup.find("section", class_="o-Ingredients")
        ingredients = []
        if ingredients_section:
            ingredient_tags = ingredients_section.find_all("p", class_="o-Ingredients__a-Ingredient")
            ingredients = [ingredient.text.strip() for ingredient in ingredient_tags]
        
        # Extract instructions
        instructions_section = soup.find("section", class_="o-Method")
        instructions = []
        if instructions_section:
            instruction_tags = instructions_section.find_all("li", class_="o-Method__m-Step")
            instructions = [instruction.text.strip() for instruction in instruction_tags]
        
        # Store data in dictionary
        recipe_data = {
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions
        }
        
        # Save to JSON file
        with open("recipe.json", "w", encoding="utf-8") as json_file:
            json.dump(recipe_data, json_file, indent=4, ensure_ascii=False)
        
        logging.info("Recipe data saved successfully to recipe.json")
        
        return recipe_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# URL to scrape
recipe_url = "https://www.foodnetwork.com/recipes/food-network-kitchen/extra-creamy-cacio-e-uova-with-grated-egg-12646498"
scraped_data = scrape_recipe(recipe_url)
print(json.dumps(scraped_data, indent=4, ensure_ascii=False))
