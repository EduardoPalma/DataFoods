import json

from recipe.dto.RecipeDto import RecipeDTO


def to_json_recipes(recipes: [RecipeDTO]):
    json_data = [recipe.to_json() for recipe in recipes]
    with open("load/recetas.json", 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)
