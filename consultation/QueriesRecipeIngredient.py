import time
from consultation.ElasticSearch import Elastic
from consultation.NutrifoodsDB import NutrifoodDB
from consultation.Translate import Translate
import datetime
from logs import Records
from logs.Records import Logs
import sys


class QueriesRecipeIngredient:
    def __init__(self):
        self.client = Elastic("localhost", "9200", "GSc_a89P7pd*6*m6Q0oF")
        self.client_nutrifoods = NutrifoodDB('nutrifoods_db', 'nutrifoods_dev', 'MVmYneLqe91$', 'localhost', '5432')

    def recipes_spanish(self, size_recipes):
        recipes = self.client.get_recipe_batch(size_recipes, self.consult_logs(), "es")
        total = len(recipes)
        for index, recipe in enumerate(recipes, start=1):
            try:
                recipe.ingredients_translate = Translate.translate_google(recipe.ingredients, 'en')
                log = Logs(recipe.id_image, 'consult', datetime.datetime.now())
                self.client.insert_logs(log.tojson(), "logs-consult")
                time.sleep(0.5)
                porcentage_ = int((index / total) * 100)
                sys.stdout.write(
                    "\rTraduciendo recetas [ES-EN] : [%-40s] %d%%" % ('=' * (index * 40 // total), porcentage_))
                sys.stdout.flush()
            except:
                print("Error Traduccion 'GoogleTranslate'")
                raise

        sys.stdout.write("\n")
        return recipes

    def recipes_english(self, size_recipes):
        recipes = self.client.get_recipe_batch(size_recipes, self.consult_logs(), "en")
        return recipes

    def consult_logs(self):
        logs = self.client.get_consult_logs("logs-consult")
        return Records.get_logs(logs)

    def queries_ingredient_nutrifoods(self):
        ingredients = self.client_nutrifoods.get_ingredient_measure()
        return ingredients

    def queries_ingredient_synonym(self):
        ingredient_synonym = self.client_nutrifoods.get_ingredient_synonyms()
        return ingredient_synonym
