from recipe.entities.IngredientNutri import IngredientIntegration
from recipe.entities.Recipe import Recipe
from ingredient_parser import parse_ingredient


def acquisition_ing_unit_quantity(recipes: list[Recipe], language: str):
    def parse(ingredients: list[str]):
        for ingredient in ingredients:
            parser = parse_ingredient(ingredient)
            if parser.name is not None:
                ingredient = parser.name.text
            else:
                # registro
                ingredient = None
            if parser.amount is not None and len(parser.amount) > 0:
                quantity = parser.amount[0].quantity
                unit = parser.amount[0].unit
            else:
                quantity = None
                unit = None
            ingredient_par = IngredientIntegration(ingredient, unit, quantity)
            recipe.ingredient_parser.append(ingredient_par)

    for recipe in recipes:
        if language == 'es':
            parse(recipe.ingredients_translate)
        else:
            parse(recipe.ingredients)
