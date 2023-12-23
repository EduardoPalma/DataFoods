from consultation.elastic_search import Elastic
from integration.acquisition_ingredient import acquisition_ing_unit_quantity
from integration.association_with_nutrifoods import association_with_nutrifoods_ingredient
from integration.cleaning import cleaning
from integration.normalization import normalization
from load.load_recipes import APIloadNutrifood
from logs.data_quality import logs_metrics_data_quality
from recipe.entities.recipe import Recipe
from recipe.entities.ingredient_nutrifood import IngredientNutri, IngredientSynonym
from utils.jsonfiles import to_json_recipes

punished = ["nutella", "nesquik", "nestle", "gourmet", "masa de hoja", "masa para pizza sin gluten"]


def pipeline(recipes: list[Recipe], ingredient_nutrifoods: list[IngredientNutri],
             ingredient_synonym: list[IngredientSynonym], language: str, client_elastic: Elastic,
             urls_nutrifoods: list[str]):
    def business_rules(recipes_normalization: list[Recipe]):
        filtered_recipes = [recipe for recipe in recipes_normalization if
                            not any(ingredient.name in punished for ingredient in recipe.ingredient_parser)]
        return filtered_recipes

    load_recipes = APIloadNutrifood("https://localhost:7212/", "api/v1/recipes/batch-insert")
    print("---------- Fase de Integracion ---------")
    acquisition_ing_unit_quantity(recipes, language)
    recipes_ = cleaning(recipes, urls_nutrifoods)
    normalization(recipes_, ingredient_synonym, language)
    business_rules(recipes_)
    recipes_association = association_with_nutrifoods_ingredient(recipes_, ingredient_nutrifoods, language,
                                                                 client_elastic)
    print("-----------  Fase de Carga ------------")
    load_recipes.send_data(recipes_association)
    logs_metrics_data_quality(client_elastic, recipes_, recipes, recipes_association, language)
    to_json_recipes(recipes_association)
    print("Recetas aptan para la insercion : ", len(recipes_association))
    print("Recetas normalizadas : ", len(recipes_))
