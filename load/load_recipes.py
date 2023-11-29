import requests

from recipe.dto.recipe_dto import RecipeDTO


class APIloadNutrifood:
    def __init__(self, base_url, endpoint):
        self.base_url = base_url
        self.endpoint = endpoint

    def send_data(self, recipes: [RecipeDTO]):
        url = f"{self.base_url}/{self.endpoint}"
        json_data = [recipe.to_json() for recipe in recipes]
        headers = {'Content-Type': 'application/json'}
        for i in range(0, len(json_data), 20):
            try:
                response = requests.post(url, data=json_data[i:i+20], headers=headers)
                if response.status_code == 200:
                    print("Solicitud exitosa:")
                    print(response.json())
                else:
                    print(f"Error en la solicitud. Código de estado: {response.status_code}")
                    print(response.text)
            except Exception as e:
                print(f"Error al realizar la solicitud: {str(e)}")
