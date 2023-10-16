from integration.AcquisitionIngredient import acquisition_ing_unit_quantity
from integration.AssociationWithNutrifoods import association_with_nutrifoods_ingredient
from integration.Cleaning import cleaning
from integration.Normalization import normalization
from recipe.entities.Recipe import Recipe
from recipe.entities.IngredientNutri import IngredientNutri, IngredientIntegration, IngredientSynonym

punished = ["nutella", "nesquik", "nestle", "gourmet", "masa de hoja", "masa para pizza sin gluten"]


def pipeline(recipes: list[Recipe], ingredient_nutrifoods: list[IngredientNutri],
             ingredient_synonym: list[IngredientSynonym], language: str):
    def business_rules(recipes_: list[Recipe]):
        filtered_recipes = [recipe for recipe in recipes_ if
                            not any(ingredient.name in punished for ingredient in recipe.ingredient_parser)]
        return filtered_recipes

    acquisition_ing_unit_quantity(recipes, language)
    recipes = cleaning(recipes)
    normalization(recipes, ingredient_synonym)
    business_rules(recipes)
    association_with_nutrifoods_ingredient(recipes, ingredient_nutrifoods)
    return recipes
