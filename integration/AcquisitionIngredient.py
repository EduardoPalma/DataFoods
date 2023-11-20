from recipe.entities.IngredientNutri import IngredientIntegration
from recipe.entities.Recipe import Recipe
from ingredient_parser import parse_ingredient
import sys
import time


def acquisition_ing_unit_quantity(recipes: list[Recipe], language: str):
    def parse(ingredients: list[str]):
        for ingredient in ingredients:
            parser = parse_ingredient(ingredient)
            if parser.name is not None:
                ingredient = parser.name.text
            else:
                ingredient = None
            if parser.amount is not None and len(parser.amount) > 0:
                quantity = parser.amount[0].quantity
                unit = parser.amount[0].unit
            else:
                quantity = None
                unit = None
            ingredient_par = IngredientIntegration(ingredient, unit, quantity)
            recipe.ingredient_parser.append(ingredient_par)

    total = len(recipes)
    for index, recipe in enumerate(recipes, start=1):
        if language == 'es':
            parse(recipe.ingredients_translate)
        else:
            parse(recipe.ingredients)

        time.sleep(0.1)
        percentage = int((index / total) * 100)
        sys.stdout.write(
            "\rAdquiriendo Ingredientes    : [%-40s] %d%%" % ('=' * (index * 40 // total),
                                                           percentage))
        sys.stdout.flush()
    sys.stdout.write("\n")
