import json

from elasticsearch import Elasticsearch

from recipe.entities.recipe import Recipe


class Elastic:
    def __init__(self, ip, port, pw):
        self.ip = ip
        self.port = port
        self.pw = pw
        self.client = self.connect()

    def connect(self):
        return Elasticsearch(f"https://{self.ip}:{self.port}",
                             ca_certs="C:/Users/hello/Documents/Rinformacion/elasticsearch-8.7.1/config/certs/http_ca"
                                      ".crt",
                             basic_auth=("elastic", self.pw))

    def get_recipe(self, size_recipe, category="es"):
        if category == "en":
            resp = self.client.search(index="recipes-es", size=size_recipe)
        else:
            resp = self.client.search(index="recipes-en", size=size_recipe)
        return Recipe.get_recipes(resp)

    def get_recipe_batch(self, size_recipe, logs, category="es"):
        consult = {
            "query": {
                "bool": {
                    "must_not": [
                        {"terms": {"name.keyword": logs}}
                    ]
                }
            },
            "size": size_recipe
        }
        if category == "es":
            resp = self.client.search(index="recipes-es", body=consult)
        else:
            resp = self.client.search(index="recipes-en", body=consult)
        return Recipe.get_recipes(resp)

    def insert_logs(self, logs, _index):
        result = self.connect().index(index=_index, document=logs)
        if result['result'] != 'created':
            print("Insercion de registro fallada")

    def get_logs_recipe(self, index):
        resp = self.client.search(index=index, size=5000)
        return resp

    def insert_logs_recipes(self, logs, _index):
        result = self.client.index(index=_index, document=logs)
        if result['result'] != 'created':
            print("Insercion de registro fallada")
