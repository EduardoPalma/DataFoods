import json
import sys
import time
import requests
import aiohttp
from recipe.dto.recipe_dto import RecipeDTO
import urllib3

from utils import jsonfiles

urllib3.disable_warnings()
headers = {'Content-Type': 'application/json'}


async def response_insert_recipe(url, data_to_send):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data_to_send, headers=headers, ssl=False) as response:
            return response


async def response_update_units(url, data_to_send):
    async with aiohttp.ClientSession() as session:
        async with session.put(url, data=data_to_send, headers=headers, ssl=False) as response:
            return response


async def response_update_syno(url, data_to_send):
    async with aiohttp.ClientSession() as session:
        async with session.put(url, data=data_to_send, headers=headers, ssl=False) as response:
            return response


def data_units():
    return jsonfiles.to_json_units()


def data_synonyms():
    return jsonfiles.to_json_synonyms()


class APIloadNutrifood:
    def __init__(self, base_url, endpoint):
        self.base_url = base_url
        self.endpoint = endpoint

    def send_data(self, recipes: [RecipeDTO]) -> tuple[bool, list[tuple[str, str]]]:
        url = f"{self.base_url}{self.endpoint}"
        json_data = [recipe.to_json() for recipe in recipes]
        response_error: [(str, str)] = []
        total = len(json_data)
        for i in range(0, total, 20):
            try:
                end_index = min(i + 20, total)
                data_to_send = json.dumps(json_data[i:end_index])
                response = requests.post(url, data=data_to_send, headers=headers, verify=False)
                time.sleep(0.5)
                if response.status_code != 200:
                    print(f"Error en la solicitud. Código de estado: {response.status_code}")
                    print(response.text)
                else:
                    response_objects = response.json()
                    for recipe in response_objects:
                        if recipe['isSuccessful']:
                            for measure_log in recipe['measureLogs']:
                                if measure_log['exists'] is False:
                                    response_error.append((recipe['name'], 'measure'))
                        else:
                            response_error.append((recipe['name'], 'measure'))

            except Exception as e:
                print(f"Error al realizar la solicitud: {str(e)}")

            time.sleep(0.05)
            percentage = int((i / total) * 100)
            sys.stdout.write(
                "\rIngresando Datos            : [%-40s] %d%%" % ('=' * (i * 40 // total),
                                                                  percentage))
            sys.stdout.flush()

        sys.stdout.write("\n")
        if not response_error:
            return True, []
        return False, response_error

    async def send_data_json(self, json_data_):
        url = f"{self.base_url}{self.endpoint}"
        total = len(json_data_)
        for i in range(0, total, 20):
            try:
                end_index = min(i + 20, total)
                data_to_send = json.dumps(json_data_[i:end_index])
                response = await response_insert_recipe(url, data_to_send)
                time.sleep(0.5)
                if response.status != 200:
                    print(f"Error en la solicitud. Código de estado: {response.status}")
                    print(response.text)

            except Exception as e:
                print(f"Error al realizar la solicitud: {str(e)}")

            time.sleep(0.05)
            percentage = int((i / total) * 100)
            sys.stdout.write(
                "\rIngresando Datos            : [%-40s] %d%%" % ('=' * (i * 40 // total),
                                                                  percentage))
            sys.stdout.flush()
        sys.stdout.write("\n")

    async def send_data_syno_unit(self, endpoint_units, endpoint_syno):
        url_units = f"{self.base_url}{endpoint_units}"
        url_syno = f"{self.base_url}{endpoint_syno}"
        units = data_units()
        synonyms = data_synonyms()
        try:
            response_unit = await response_update_units(url_units, units)
            response_syno = await response_update_syno(url_syno, synonyms)
            if response_unit.status != 200 and response_syno.status != 200:
                print(f"Error en la solicitud. Código de estado: {response_unit.status}")
                print(response_unit.text)
        except Exception as e:
            print(f"Error al realizar la solicitud: {str(e)}")
