from consultation.ElasticSearch import Elastic
from consultation.Translate import Translate


class RecipeQueries:
    def __init__(self):
        self.client = Elastic("localhost", "9200", "GSc_a89P7pd*6*m6Q0oF")

    def recipes_spanish(self, size_recipes):
        recipes = self.client.get_recipe_es(size_recipes)

        for recipe in recipes:
            recipes_translate = []
            try:
                for ingredient_text in recipe.ingredients:
                    translate_ingredient = Translate.translate_google(ingredient_text, "en")
                    recipes_translate.append(translate_ingredient)

                recipe.ingredients_translate = recipes_translate
            except:
                print("error translate ingredient text 'save modulo error'")

        return recipes

    def recipes_english(self, size_recipes):
        recipes = self.client.get_recipe_en(size_recipes)
        return recipes
