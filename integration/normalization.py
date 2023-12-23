import time
import sys
import re
from unidecode import unidecode
from consultation.translate import Translate
from recipe.entities.ingredient_nutrifood import IngredientIntegration, IngredientSynonym
from recipe.entities.recipe import Recipe
from fractions import Fraction

dictionary_food_category = {
    "Plato de entrada": ["entrada", "aperitivos", "refrigerios", "aperitivo", "postres y refrigerios"],
    "Bebida": ["bebidas"],
    "Ensalada": ["ensaladas", "ensalada"],
    "Pan": ["panes"],
    "Plato principal": ["comidas", "comida", "platos principales", "plato principal",
                        "guarniciones", "saludables"],
    "Postre": ["postres", "postre", "postres y refrigerios"],
    "Reposteria": [""],
    "Salsa": ["salsas"],
    "Sándwich": ["sandwich"],
    "Sopa": ["sopas"],
    "Vegetariano": ["vegetariano"],
    "Vegano": ["vegano"]}

dictionary_meals_day = {"Desayuno": ["desayuno"], "Almuerzo": ["almuerzo"], "Cena": ["cena"],
                        "Merienda": ["Snack", "snack"]}

dictionary_difficulty = {"Fácil": ["facil", "fácil", "Facil"], "Mediana": ["media"], "Difícil": ["dificil"]}

dictionary_unit = {"kg": ["kilogramo", "kilogramos"], "g": ["grs", "gramos", "gramo"], "oz": ["onza", "onzas"],
                   "lb": ["libra", "libras"]}

pattern = re.compile(r'Paso \d+: ')


def normalization(recipes: list[Recipe], ingredient_synonym: list[IngredientSynonym], language: str):
    def normalization_word_with_s(word: str):
        words = word.split()
        words_without_s = [word_.rstrip('s') for word_ in words]
        return ' '.join(words_without_s)

    def normalization_food_day(category_: str) -> str:
        for key, value in dictionary_meals_day.items():
            if category_.lower() in value:
                return key
        return category_

    def remove_dish_types(_recipe: [Recipe]):
        dish_types_remove = ["Desayuno", "Desayunos", "Condimentos"]
        for category in dish_types_remove:
            if category in _recipe.category_recipe:
                _recipe.category_recipe.remove(category)

    def normalization_food_category(category_: str) -> str:
        for key, value in dictionary_food_category.items():
            if category_.lower() in value:
                return key
        return category_

    def normalization_translate_batch(_recipe: Recipe):
        ingredients_to_translate = []
        for ingredient_text in _recipe.ingredient_parser:
            if ingredient_text.unit is None or ingredient_text.unit == '':
                trans_text = ingredient_text.name.replace(".", "")
                ingredients_to_translate.append(trans_text)
            else:
                trans_text = ingredient_text.name.replace(".", "") + "|" + ingredient_text.unit.replace(".", "")
                ingredients_to_translate.append(trans_text)

        try:
            translate = Translate.translate_google(ingredients_to_translate, 'es', 'en')
        except Exception as e:
            print("error al traducir: ", e)
            translate = Translate.translate_batch(ingredients_to_translate, 'en', 'es')

        time.sleep(0.7)
        for i, tran in enumerate(translate, start=0):
            split_tran = tran.split("|")
            if len(split_tran) == 1:
                _recipe.ingredient_parser[i].name = normalization_word_with_s(tran.strip())
            else:
                _recipe.ingredient_parser[i].name = normalization_word_with_s(split_tran[0].strip())
                _recipe.ingredient_parser[i].unit = normalization_word_with_s(split_tran[1].strip())

    def normalization_quantity(ingredient_parser: IngredientIntegration):
        if ingredient_parser.quantity == "":
            ingredient_parser.quantity = None
        elif ingredient_parser.quantity is not None:
            if "." in ingredient_parser.quantity:
                fraction = Fraction(ingredient_parser.quantity).limit_denominator()
                if fraction.numerator == 667:
                    ingredient_parser.quantity = "2/3"
                elif fraction.numerator == 333:
                    ingredient_parser.quantity = "1/3"
                else:
                    if int(ingredient_parser.quantity.split(".")[0]) >= 1:
                        a = fraction.numerator // fraction.denominator
                        b = fraction.numerator % fraction.denominator
                        ingredient_parser.quantity = str(a) + " " + str(b) + "/" + str(fraction.denominator)
                    else:
                        ingredient_parser.quantity = str(fraction.numerator) + "/" + str(fraction.denominator)
            else:
                integer_match = re.search(r'\d+', ingredient_parser.quantity)
                if integer_match:
                    ingredient_parser.quantity = integer_match.group()

    def normalization_unit(ingredient_par_: IngredientIntegration):
        if ingredient_par_.unit is not None:
            if "cda" in ingredient_par_.unit:
                ingredient_par_.unit = "Cucharada"
            if "tbsps" in ingredient_par_.unit:
                ingredient_par_.unit = "Cucharada"
            for key, value in dictionary_unit.items():
                if ingredient_par_.unit.lower() in value:
                    ingredient_par_.unit = key

    def normalization_difficulty(recipe_: Recipe):
        for key, value in dictionary_difficulty.items():
            if recipe_.difficulty.lower() in value:
                return key

    def normalization_ingredient_name(ingredient_parser: IngredientIntegration):
        for ingredient_syno in ingredient_synonym:
            for synonym in ingredient_syno.synonym:
                if unidecode(ingredient_parser.name.lower()) == unidecode(synonym.lower().rstrip('s')):
                    ingredient_parser.name = ingredient_syno.name

    def translate_steps(steps: [str]):
        trans_es = Translate.translate_google(steps, 'es', 'en')
        time.sleep(0.5)
        return trans_es

    def translate_name(name_recipe: str):
        trans_es = Translate.translate_google_single(name_recipe, 'es', 'en')
        time.sleep(0.5)
        return trans_es

    total = len(recipes)
    for index, recipe in enumerate(recipes, start=1):
        normalization_translate_batch(recipe)
        for ingredient_par in recipe.ingredient_parser:
            normalization_unit(ingredient_par)
            normalization_quantity(ingredient_par)
            normalization_ingredient_name(ingredient_par)

        if language == 'en':
            recipe.steps = translate_steps(recipe.steps)
            recipe.name_recipe_translate = translate_name(recipe.name_recipe)

        recipe.food_days = [normalization_food_day(category_meals_day) for category_meals_day in recipe.food_days]
        recipe.category_recipe = [category for category in recipe.category_recipe if category != ""]
        recipe.category_recipe = [normalization_food_category(category_recipe) for category_recipe in
                                  recipe.category_recipe]
        recipe.category_recipe = list(set(recipe.category_recipe))
        remove_dish_types(recipe)
        recipe.difficulty = normalization_difficulty(recipe)
        recipe.steps = [pattern.sub('', step) for step in recipe.steps]

        time.sleep(0.05)
        percentage = int((index / total) * 100)
        sys.stdout.write(
            "\rNormalizando Datos          : [%-40s] %d%%" % ('=' * (index * 40 // total),
                                                              percentage))
        sys.stdout.flush()
    sys.stdout.write("\n")
    return recipes
