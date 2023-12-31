import time
from consultation.elastic_search import Elastic
from consultation.nutri_foods_db import NutrifoodDB
from consultation.translate import Translate
from logs.records import get_logs_recipes
import sys


class QueriesRecipeIngredient:
    def __init__(self):
        self.client = Elastic("localhost", "9200", "GSc_a89P7pd*6*m6Q0oF")
        self.client_nutrifoods = NutrifoodDB('nutrifoods_db', 'nutrifoods_dev', 'MVmYneLqe91$', 'localhost', '5432')

    def recipes_spanish(self, size_recipes):
        recipes = self.client.get_recipe_batch(size_recipes,
                                               get_logs_recipes(self.client.get_logs_recipe("logs-recipe"), "es"), "es")
        total = len(recipes)
        for index, recipe in enumerate(recipes, start=1):
            try:
                recipe.ingredients_translate = Translate.translate_google(recipe.ingredients, 'en')
                time.sleep(0.8)
                percentage_ = int((index / total) * 100)
                sys.stdout.write(
                    "\rTraduciendo recetas [ES-EN] : [%-40s] %d%%" % ('=' * (index * 40 // total), percentage_))
                sys.stdout.flush()
            except:
                print("Error Traduccion 'GoogleTranslate'")
                raise

        sys.stdout.write("\n")
        return recipes

    def recipes_english(self, size_recipes):
        recipes = self.client.get_recipe_batch(size_recipes,
                                               get_logs_recipes(self.client.get_logs_recipe("logs-recipe"), "en"), "en")
        return recipes

    def queries_ingredient_nutrifoods(self):
        ingredients = self.client_nutrifoods.get_ingredient_measure()
        return ingredients

    def queries_ingredient_synonym(self):
        ingredient_synonym = self.client_nutrifoods.get_ingredient_synonyms()
        return ingredient_synonym

    def queries_recipe_url(self):
        return self.client_nutrifoods.get_name_recipe_nutrifoods()
