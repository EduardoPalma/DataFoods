import json

from recipe.dto.recipe_dto import RecipeDTO


def to_json_recipes(recipes: [RecipeDTO]):
    try:
        try:
            with open("analysis/recetas.json", 'r', encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            existing_data = []

        json_data = existing_data + [recipe.to_json() for recipe in recipes]
        with open("analysis/recetas.json", 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Error al agregar datos al archivo JSON: {str(e)}")
