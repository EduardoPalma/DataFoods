import sys
import time

from consultation.elastic_search import Elastic
from logs.records import LogsIngredientFailsMeasure, LogsIngredientFails, add_logs_measure, add_logs_ingredient, \
    save_logs_recipes, save_logs_ingredient_fails, save_logs_ingredient_measure_fails
from recipe.dto.recipe_dto import RecipeDTO, QuantityDto, MeasuresDto
from recipe.entities.ingredient_nutrifood import IngredientNutri, IngredientIntegration
from recipe.entities.recipe import Recipe
import spacy
from unidecode import unidecode
from utils.utils_unit import quantity_frac, quantity_unit
from utils.nlp_utils import stemmer_porter

nlp = spacy.load("es_core_news_lg")
punishable_ingredient = ["sal", "té", "ron", "ajo", "azúcar"]


def association_with_nutrifoods_ingredient(recipes: list[Recipe], ingredient_nutrifoods: list[IngredientNutri],
                                           language: str, client_elastic: Elastic):
    def search_ingredient_nutrifoods(ingredient_: str) -> IngredientNutri | None:
        for ingredient_nutrifood in ingredient_nutrifoods:
            if unidecode(ingredient_nutrifood.name.lower().strip().rstrip('s')) == ingredient_.lower():
                return ingredient_nutrifood
        return None

    def search_for_ingredient_contained_within_text(ingredient_, ingredient_nutrifoods_clean):
        for ingredient_nutrifood in ingredient_nutrifoods_clean:
            if unidecode(ingredient_nutrifood.name.lower().strip().rstrip("s")) in ingredient_.lower():
                return ingredient_nutrifood
        return None

    def search_ingredient_nutrifoods_contains(ingredient_: str) -> IngredientNutri | None:
        def similarity_contains_ingredient_nutrifoods(value: 1, _ingredient_similarity, _coincidences: [],
                                                      _ingredient_nutrifoods_clean):
            if value == 1:
                for ingredient_nutrifood in ingredient_nutrifoods:
                    if ingredient_.lower() in unidecode(ingredient_nutrifood.name.lower().strip().rstrip('s')):
                        ingredient_similarity_nutrifood = nlp(unidecode(ingredient_nutrifood.name.lower().strip()))
                        if ingredient_similarity_nutrifood.has_vector and _ingredient_similarity.has_vector:
                            similarity = _ingredient_similarity.similarity(ingredient_similarity_nutrifood)
                            _coincidences.append((ingredient_nutrifood, similarity))
            else:
                _coincidences.clear()
                for ingredient_nutrifood in _ingredient_nutrifoods_clean:
                    if unidecode(ingredient_nutrifood.name.lower().strip().rstrip('s')) in ingredient_.lower():
                        ingredient_similarity_nutrifood = nlp(unidecode(ingredient_nutrifood.name.lower().strip()))
                        if ingredient_similarity_nutrifood.has_vector and _ingredient_similarity.has_vector:
                            similarity = ingredient_similarity_nutrifood.similarity(_ingredient_similarity)
                            _coincidences.append((ingredient_nutrifood, similarity))

        coincidences = []
        ingredient_nutrifoods_clean = [ingredient_aux for ingredient_aux in ingredient_nutrifoods if
                                       ingredient_aux.name.lower() not in punishable_ingredient]
        if ingredient_ == "":
            return None
        ingredient_similarity = nlp(ingredient_.lower())
        similarity_contains_ingredient_nutrifoods(1, ingredient_similarity, coincidences, ingredient_nutrifoods_clean)

        if coincidences:
            max_similarity = max(coincidences, key=lambda t: t[1])
            return max_similarity[0]

        else:
            similarity_contains_ingredient_nutrifoods(2, ingredient_similarity, coincidences,
                                                      ingredient_nutrifoods_clean)
            if coincidences:
                max_similarity = max(coincidences, key=lambda t: t[1])
                if max_similarity[1] >= 0.5:
                    return max_similarity[0]
                else:
                    return search_for_ingredient_contained_within_text(ingredient_, ingredient_nutrifoods_clean)
            else:
                return search_for_ingredient_contained_within_text(ingredient_, ingredient_nutrifoods_clean)

    def search_ingredient_unit(ingredient_nutrifood: IngredientNutri, unit_ingredient: str,
                               quantity_ingredient) -> QuantityDto | MeasuresDto | None:
        if unit_ingredient is None or unit_ingredient == "":
            for unit in ingredient_nutrifood.measures:
                if unit.name.lower() == 'unidad':
                    fraction = quantity_frac(quantity_ingredient)
                    return MeasuresDto(unit.name, ingredient_nutrifood.name, fraction[0], fraction[1], fraction[2])
            return None

        if unit_ingredient == "pizca" or unit_ingredient == "pellizco":
            return QuantityDto(ingredient_nutrifood.name, 0)

        if ("g" == unit_ingredient or "lb" in unit_ingredient or "ml" in unit_ingredient or
                "oz" == unit_ingredient or "kg" in unit_ingredient):
            grams = quantity_unit(unit_ingredient, quantity_ingredient)
            return QuantityDto(ingredient_nutrifood.name, grams)

        unit = stemmer_porter(nlp(unit_ingredient.lower()))
        for unit_ingredient_nutrifood in ingredient_nutrifood.measures:
            if (stemmer_porter(
                    nlp(unidecode(unit_ingredient_nutrifood.name.lower()))) in unit or unit in stemmer_porter(
                nlp(unidecode(unit_ingredient_nutrifood.name.lower()))) or
                    unidecode(unit_ingredient_nutrifood.name.lower()) in unit_ingredient.lower()):
                fraction = quantity_frac(quantity_ingredient)
                return MeasuresDto(unit_ingredient_nutrifood.name, ingredient_nutrifood.name, fraction[0], fraction[1],
                                   fraction[2])
        return None

    def match_unit_quantity(_ingredient, ingredient_nutri_, _recipe_dto):
        if _ingredient.quantity is not None:
            measures = search_ingredient_unit(ingredient_nutri_, _ingredient.unit.lower(),
                                              _ingredient.quantity)
            if measures is not None:
                if isinstance(measures, MeasuresDto):
                    _recipe_dto.measures.append(measures)
                else:
                    _recipe_dto.quantities.append(measures)
                return True
            else:
                add_logs_measure(ingredient_nutri_.name, _ingredient.unit.lower(),
                                 log_measures_ingredient_fails, recipe.url, _ingredient.name, language)
                return False
        else:
            _recipe_dto.quantities.append(QuantityDto(ingredient_nutri_.name, 0))
            return True

    def nlp_association_ingredient(_ingredient_nutri: IngredientNutri, _ingredient: IngredientIntegration,
                                   recipe_dto_: RecipeDTO):
        if "agua" in _ingredient.name.lower():
            return True
        if _ingredient_nutri is None:
            ingredient_nutri_ = search_ingredient_nutrifoods_contains(text_normalized)
            if ingredient_nutri_ is None:
                add_logs_ingredient(log_ingredient_fails, _ingredient.name.lower(), recipe.url, language)
                return False
            else:
                return match_unit_quantity(_ingredient, ingredient_nutri_, recipe_dto_)
        else:
            return match_unit_quantity(_ingredient, _ingredient_nutri, recipe_dto_)

    log_measures_ingredient_fails: [LogsIngredientFailsMeasure] = []
    log_ingredient_fails: [LogsIngredientFails] = []
    recipe_correct = True
    recipes_associated_with_nutrifoods: [RecipeDTO] = []
    logs_recipe_correct: [(str, str)] = []
    total = len(recipes)
    for index, recipe in enumerate(recipes, start=1):

        recipe_dto = RecipeDTO(recipe.name_recipe, recipe.author, recipe.url, recipe.portions, recipe.preparation_time,
                               recipe.difficulty, recipe.food_days, recipe.category_recipe,
                               recipe.steps) if language == "es" else RecipeDTO(recipe.name_recipe_translate,
                                                                                recipe.author,
                                                                                recipe.url, recipe.portions,
                                                                                recipe.preparation_time,
                                                                                recipe.difficulty, recipe.food_days,
                                                                                recipe.category_recipe, recipe.steps)
        for ingredient in recipe.ingredient_parser:
            text_normalized = unidecode(ingredient.name.lower().strip().replace(".", ""))
            ingredient_nutri: [IngredientNutri] = search_ingredient_nutrifoods(text_normalized)
            recipe_correct = nlp_association_ingredient(ingredient_nutri, ingredient, recipe_dto)
            if recipe_correct is False:
                break

        if recipe_correct:
            logs_recipe_correct.append((recipe.id_image, recipe.name_recipe))
            recipes_associated_with_nutrifoods.append(recipe_dto)

        time.sleep(0.05)
        percentage = int((index / total) * 100)
        sys.stdout.write(
            "\rAsociando Ingredientes      : [%-40s] %d%%" % ('=' * (index * 40 // total),
                                                              percentage))
        sys.stdout.flush()

    sys.stdout.write("\n")
    save_logs_ingredient_fails(log_ingredient_fails, client_elastic)
    save_logs_ingredient_measure_fails(log_measures_ingredient_fails, client_elastic)
    save_logs_recipes(logs_recipe_correct, language, client_elastic)
    return recipes_associated_with_nutrifoods
