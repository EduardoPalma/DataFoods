import asyncio
import json

from load.load_recipes import APIloadNutrifood


async def insert_recipe(archivo_json):
    load_recipes = APIloadNutrifood("https://localhost:7212/", "api/v1/recipes/multiple")
    with open(archivo_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
        await load_recipes.send_data_json(data)


if __name__ == '__main__':
    asyncio.run(insert_recipe("analysis/recetas.json"))
