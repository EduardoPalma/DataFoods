from consultation.ElasticSearch import Elastic
from consultation.Translate import Translate
import datetime

from logs import Records
from logs.Records import Logs


class RecipeQueries:
    def __init__(self):
        self.client = Elastic("localhost", "9200", "GSc_a89P7pd*6*m6Q0oF")

    def recipes_spanish(self, size_recipes):
        recipes = self.client.get_recipe_batch(size_recipes, self.consult_logs(), "es")
        for recipe in recipes:
            try:
                recipe.ingredients_translate = Translate.translate_google(recipe.ingredients, 'en')
                log = Logs(recipe.id_image, 'consult', datetime.datetime.now())
                self.client.insert_logs(log.tojson(), "logs-consult")
                print("Receta traducida :" + recipe.id_image)
            except:
                print("Error Traduccion 'GoogleTranslate'")
                raise
        return recipes

    def recipes_english(self, size_recipes):
        recipes = self.client.get_recipe_batch(size_recipes, self.consult_logs(), "en")
        return recipes

    def consult_logs(self):
        logs = self.client.get_consult_logs("logs-consult")
        return Records.get_logs(logs)
