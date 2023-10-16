from consultation.Translate import Translate
from recipe.entities.IngredientNutri import IngredientIntegration, IngredientSynonym
from recipe.entities.Recipe import Recipe
from fractions import Fraction

dictionary_food_category = {
    "Plato de entrada": ["entrada", "aperitivos", "refrigerios", "aperitivo", "postres y refrigerios"],
    "Bebida": ["bebidas"],
    "Ensalada": ["ensaladas", "ensalada"],
    "Pan": ["panes"],
    "Plato principal": ["comidas", "comida", "platos principales", "plato principal",
                        "guarniciones", "saludables"],
    "Postre": ["postres", "postre"],
    "Reposteria": [""],
    "Salsa": ["salsas"],
    "Sándwich": ["sandwich"],
    "Sopa": ["sopas"],
    "Vegetariano": ["vegetariano"],
    "Vegano": ["vegano"]}

dictionary_meals_day = {"Desayuno": ["desayuno"], "Almuerzo": ["almuerzo"], "Cena": ["cena"],
                        "Merienda": ["Snack", "snack"]}

dictionary_dificulty = {"Fácil": ["facil", "fácil"], "Medianada": ["media"], "Dificil": ["dificil"]}


def normalization(recipes: list[Recipe], ingredient_synonym: list[IngredientSynonym]):
    def normalization_food_day(category_: str) -> str:
        for key, value in dictionary_meals_day.items():
            if category_.lower() in value:
                return key
        return category_

    def normalization_food_category(category_: str) -> str:
        for key, value in dictionary_food_category.items():
            if category_.lower() in value:
                return key
        return category_

    def normalization_unit(ingredient_parser: IngredientIntegration):
        if ingredient_parser.unit is None:
            trans_en = ingredient_parser.name
            trans_es = Translate.translate_google_single(trans_en, 'es', 'en')
            ingredient_parser.name = trans_es
        else:
            trans_en = ingredient_parser.name + "|" + ingredient_parser.unit
            trans_es = Translate.translate_google_single(trans_en, 'es', 'en')
            split = trans_es.split("|")
            ingredient_parser.name = split[0]
            ingredient_parser.unit = split[1]

    def normalization_quantity(ingredient_parser: IngredientIntegration):
        if ingredient_parser.quantity is not None:
            if "." in ingredient_parser.quantity:
                fraction = Fraction(ingredient_parser.quantity).limit_denominator()
                if fraction.numerator == 667:
                    ingredient_parser.quantity = "2/3"
                elif fraction.numerator == 333:
                    ingredient_parser.quantity = "1/3"
                else:
                    ingredient_parser.quantity = str(fraction.numerator) + "/" + str(fraction.denominator)

    def normalization_difficulty(recipe_: Recipe):
        for key, value in dictionary_dificulty.items():
            if recipe_.difficulty.lower() in value:
                return key

    def normalization_ingredient_name(ingredient_parser: IngredientIntegration):
        for ingredient_syno in ingredient_synonym:
            if ingredient_parser.name in ingredient_syno.synonym:
                print("okey", ingredient_parser.name)

    for recipe in recipes:
        for ingredient_par in recipe.ingredient_parser:
            normalization_unit(ingredient_par)
            normalization_quantity(ingredient_par)
            normalization_ingredient_name(ingredient_par)

        recipe.food_days = [normalization_food_day(category_meals_day) for category_meals_day in recipe.food_days]
        recipe.category_recipe = [category for category in recipe.category_recipe if category != ""]
        recipe.category_recipe = [normalization_food_category(category_recipe) for category_recipe in
                                  recipe.category_recipe]
        normalization_difficulty(recipe)
