import csv
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


def to_json_units():
    try:
        with open('analysis/new_synonyms/units_ingredient.csv', mode='r', encoding='utf-8') as file_csv:
            read_csv = csv.reader(file_csv)
            next(read_csv)
            data = []
            for row in read_csv:
                ingredient = row[0]
                units = row[1].split('|')
                units_json = []
                for unit in units:
                    name_unit = unit.split(';')[0]
                    grams = unit.split(';')[1]
                    json_u = {
                        'name': name_unit.capitalize(),
                        'grams': float(grams)
                    }
                    units_json.append(json_u)
                data_json = {
                    'ingredient': ingredient.capitalize(),
                    'measures': units_json
                }
                data.append(data_json)

        json_result = json.dumps(data, ensure_ascii=False, indent=2)
        return json_result

    except Exception as e:
        print(f'Error al procesar el archivo CSV: {str(e)}')


def to_json_synonyms():
    with open('analysis/new_synonyms/synonyms.csv', mode='r', encoding='utf-8') as file_csv:
        read_csv = csv.reader(file_csv)
        next(read_csv)
        data = []
        for row in read_csv:
            ingredient = row[0]
            syno = row[1].split(';')
            data_json = {
                'ingredient': ingredient.capitalize(),
                'synonyms': [sy.title() for sy in syno]
            }
            data.append(data_json)
    json_result = json.dumps(data, ensure_ascii=False, indent=2)
    return json_result
