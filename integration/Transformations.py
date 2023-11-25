import datetime
from consultation.ElasticSearch import Elastic
from integration.AcquisitionIngredient import acquisition_ing_unit_quantity
from integration.AssociationWithNutrifoods import association_with_nutrifoods_ingredient
from integration.Cleaning import cleaning
from integration.Normalization import normalization
from recipe.entities.Recipe import Recipe
from recipe.entities.IngredientNutrifood import IngredientNutri, IngredientSynonym
from utils.jsonfiles import to_json_recipes

punished = ["nutella", "nesquik", "nestle", "gourmet", "masa de hoja", "masa para pizza sin gluten"]


def pipeline(recipes: list[Recipe], ingredient_nutrifoods: list[IngredientNutri],
             ingredient_synonym: list[IngredientSynonym], language: str, client_elastic: Elastic):
    def business_rules(recipes_normalization: list[Recipe]):
        filtered_recipes = [recipe for recipe in recipes_normalization if
                            not any(ingredient.name in punished for ingredient in recipe.ingredient_parser)]
        return filtered_recipes

    # en el propio modulo
    def duplicity(before_recipes: int, after_recipes: int):
        duplicity_ = 1 - float(after_recipes / before_recipes)
        return {
            "duplicity": duplicity_,
            "date": datetime.datetime.now()
        }

    # en el propio modulo
    def accuracy(before_recipes: int, after_recipes: int):
        accuracy_ = float(after_recipes / before_recipes)
        return {
            "accuracy": accuracy_,
            "date": datetime.datetime.now()
        }

    print("---------- Fase de Integracion ---------")
    acquisition_ing_unit_quantity(recipes, language)
    recipes_ = cleaning(recipes)
    # en su propio modulo
    client_elastic.insert_logs(duplicity(len(recipes), len(recipes_)), "logs-duplicity")
    normalization(recipes_, ingredient_synonym)
    business_rules(recipes_)
    recipes_association = association_with_nutrifoods_ingredient(recipes_, ingredient_nutrifoods, client_elastic)
    # en su propio modulo
    client_elastic.insert_logs(accuracy(len(recipes_), len(recipes_association)), "logs-accuracy")
    # carga de datos
    to_json_recipes(recipes_association)
    return recipes_
