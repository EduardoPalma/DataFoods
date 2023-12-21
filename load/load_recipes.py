import json
import sys
import time
import requests
from recipe.dto.recipe_dto import RecipeDTO
import urllib3

urllib3.disable_warnings()


class APIloadNutrifood:
    def __init__(self, base_url, endpoint):
        self.base_url = base_url
        self.endpoint = endpoint

    def send_data(self, recipes: [RecipeDTO]):
        url = f"{self.base_url}{self.endpoint}"
        json_data = [recipe.to_json() for recipe in recipes]
        headers = {'Content-Type': 'application/json'}
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
            return True
        return False
