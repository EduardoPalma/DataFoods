from elasticsearch import Elasticsearch

from recipe.json.Recipe import Recipe


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

    def get_recipe_es(self, size_recipe):
        resp = self.client.search(index="recipes-es", size=size_recipe)
        return Recipe.get_recipes(resp)

    def get_recipe_en(self, size_recipe):
        resp = self.client.search(index="recipes-en", size=size_recipe)
        return Recipe.get_recipes(resp)

    def get_logs(self, logs):
        result = self.connect().index(index="logs-consult", document=logs)
        print(result['result'])
