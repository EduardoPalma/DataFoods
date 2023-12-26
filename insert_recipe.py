import asyncio
import json

from load.load_recipes import APIloadNutrifood


async def insert_recipe(archivo_json):
    load_recipes = APIloadNutrifood("https://localhost:7212/", "api/v1/recipes/batch-insert")
    with open(archivo_json, 'r', encoding='utf-8') as file:
        datas = json.load(file)
        datas = [data for data in datas if data.get('name') != 'Ensalada keto de atún con alcaparras']
        print(len(datas))
        await load_recipes.send_data_json(datas)


async def update_data_units_synonyms_ingredient():
    api_nutrifoods = APIloadNutrifood("https://localhost:7212/", "api/v1/recipes/batch-insert")
    await api_nutrifoods.send_data_syno_unit("api/v1/ingredients/measures/batch-update",
                                             "api/v1/ingredients/synonyms/batch-update")


if __name__ == '__main__':
    asyncio.run(update_data_units_synonyms_ingredient())
    asyncio.run(insert_recipe("analysis/recetas.json"))
