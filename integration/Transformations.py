from ingredient_parser import parse_ingredient
from recipe.entities.Recipe import Recipe
from recipe.entities.IngredientNutri import IngredientNutri, IngredientIntegration
from consultation.Translate import Translate

dictionary_meals_day = {"Desayuno": 1, "Almuerzo": 2, "Cena": 3, "Merienda": 4}


def pipeline(recipes: list[Recipe], ingredient_nutrifoods: list[IngredientNutri]):
    def acquisition_ing_unit_quantity():
        for recipe in recipes:
            for ingredient in recipe.ingredients:
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

    def cleaning():
        def duplicate_attribute(recipe_duplicate: Recipe):
            return recipe_duplicate.name_recipe

        def missing_ingredient(recipe: Recipe):
            for ingredient_par in recipe.ingredient_parser:
                if ingredient_par.name is None:
                    return False

        def missing_data(recipe_missing: Recipe):
            if recipe_missing.portions == 0:
                return False
            elif recipe_missing.name_recipe == '':
                return False
            elif len(recipe_missing.steps) == 0 or len(recipe_missing.ingredients) == 0:
                return False
            elif missing_ingredient(recipe_missing) is False:
                return False
            else:
                return True

        # duplicados y faltantes
        recipes_uniq = set()
        recipes_aux: list[Recipe] = []
        for recipe in recipes:
            if duplicate_attribute(recipe) not in recipes_uniq and missing_data(recipe):
                recipes_uniq.add(duplicate_attribute(recipe))
                recipes_aux.append(recipe)

        return recipes_aux

    def normalization(recipes_normalization: list[Recipe]):

        def normalization_food_day(category: str) -> str:
            if category == "Snack":
                return "Merienda"
            return category

        for recipe in recipes_normalization:
            for ingredient_par in recipe.ingredient_parser:
                if ingredient_par.unit is None:
                    trans_en = ingredient_par.name
                    trans_es = Translate.translate_google_single(trans_en, 'es', 'en')
                    ingredient_par.name = trans_es
                else:
                    trans_en = ingredient_par.name + "|" + ingredient_par.unit
                    trans_es = Translate.translate_google_single(trans_en, 'es', 'en')
                    split = trans_es.split("|")
                    ingredient_par.name = split[0]
                    ingredient_par.unit = split[1]

            for i, category_meals_day in enumerate(recipe.food_days):
                category = normalization_food_day(category_meals_day)
                recipe.food_days[i] = category

    # proceso de normalizacion
    # nombres de ingredientes con pertenencia en la base de datos de nutrifoods, sinonimous
    # normliazcion de las categorias

    def association_with_nutrifoods_ingredient(recipes: list[Recipe]):
        # se asocia y se busca los nombres de los ingredientes con la id correspondientes
        # ya sea el ingrediente con su id y la unidad de medida especifica
        return recipes

    def busines_rules(recipes: list[Recipe]):
        # reglas de negocio asociada al constexto
        # reglas todavia no definidas
        return recipes

    acquisition_ing_unit_quantity()
    recipes = cleaning()
    normalization(recipes)
    return recipes
    # clean_date(recipes)
    # normalization(recipes)
    # association_with_nutrifoods_ingredient(recipes)
    # busines_rules(recipes)
