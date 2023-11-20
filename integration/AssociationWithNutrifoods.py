from logs.Records import LogsIngredientFailsMeasure, LogsIngredientFails, save_logs_ingredient_fails, \
    save_ingredient_measure_fails, add_logs_measure, add_logs_ingredient
from recipe.dto.RecipeDto import RecipeDTO, QuantityDto, MeasuresDto
from recipe.entities.IngredientNutri import IngredientNutri, IngredientIntegration
from recipe.entities.Recipe import Recipe
import spacy
from unidecode import unidecode
from utils.ConvertUnits import convert_unit
from utils.Nlputils import stemmer_porter

nlp = spacy.load("es_core_news_lg")
punishable_ingredient = ["sal", "té", "ron"]


def association_with_nutrifoods_ingredient(recipes: list[Recipe], ingredient_nutrifoods: list[IngredientNutri]):
    def search_ingredient_nutrifoods(ingredient_: str) -> IngredientNutri | None:
        for ingredient_nutrifood in ingredient_nutrifoods:
            if unidecode(ingredient_nutrifood.name.lower().strip().rstrip('s')) == ingredient_:
                return ingredient_nutrifood
        return None

    def search_for_ingredient_contained_within_text(ingredient_, ingredient_nutrifoods_clean):
        for ingredient_nutrifood in ingredient_nutrifoods_clean:
            if unidecode(ingredient_nutrifood.name.lower().strip().rstrip("s")) in ingredient_:
                return ingredient_nutrifood
        return None

    def search_ingredient_nutrifoods_contains(ingredient_: str) -> IngredientNutri | None:
        def similarity_contains_ingredient_nutrifoods(value: 1, _ingredient_similarity, _coincidences: [],
                                                      _ingredient_nutrifoods_clean):
            if value == 1:
                for ingredient_nutrifood in ingredient_nutrifoods:
                    if ingredient_ in unidecode(ingredient_nutrifood.name.lower().strip().rstrip('s')):
                        ingredient_similarity_nutrifood = nlp(unidecode(ingredient_nutrifood.name.lower().strip()))
                        similarity = _ingredient_similarity.similarity(ingredient_similarity_nutrifood)
                        _coincidences.append((ingredient_nutrifood, similarity))
            else:
                _coincidences.clear()
                for ingredient_nutrifood in _ingredient_nutrifoods_clean:
                    if unidecode(ingredient_nutrifood.name.lower().strip().rstrip('s')) in ingredient_:
                        ingredient_similarity_nutrifood = nlp(unidecode(ingredient_nutrifood.name.lower().strip()))
                        similarity = ingredient_similarity_nutrifood.similarity(_ingredient_similarity)
                        _coincidences.append((ingredient_nutrifood, similarity))

        coincidences = []
        ingredient_nutrifoods_clean = [ingredient_aux for ingredient_aux in ingredient_nutrifoods if
                                       ingredient_aux.name.lower() not in punishable_ingredient]
        if ingredient_ == "":
            return None
        ingredient_similarity = nlp(ingredient_)
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

    def quantity_frac(quantity: str) -> (int, int, int):
        if '/' in quantity:
            fraction = quantity.split("/")
            if len(quantity) <= 2:
                return int(quantity), 0, 0
            elif len(quantity) == 3:
                return 0, int(fraction[0]), int(fraction[1])
            else:
                return int(fraction[0]), int(fraction[1]), int(fraction[2])
        else:
            return int(quantity), 0, 0

    def quantity_unit(unit: str, quantity_ingredient) -> float:
        if unit == "g":
            return float(quantity_ingredient)
        elif unit == "ml":
            return float(quantity_ingredient) * 1.85
        else:
            return convert_unit(unit, float(quantity_ingredient))

    def search_ingredient_unit(ingredient_nutrifood: IngredientNutri, unit_ingredient: str,
                               quantity_ingredient) -> QuantityDto | MeasuresDto | None:
        if unit_ingredient is None or unit_ingredient == "":
            for unit in ingredient_nutrifood.measures:
                if unit.name == 'unidad':
                    fraction = quantity_frac(quantity_ingredient)
                    return MeasuresDto(unit.id, fraction[0], fraction[1], fraction[2])
            return None

        if unit_ingredient == "pizca" or unit_ingredient == "pellizco":
            return QuantityDto(ingredient_nutrifood.id, 0)

        if ("g" == unit_ingredient or "lb" in unit_ingredient or "ml" in unit_ingredient or
                "oz" == unit_ingredient or "kg" in unit_ingredient):
            grams = quantity_unit(unit_ingredient, quantity_ingredient)
            return QuantityDto(ingredient_nutrifood.id, grams)

        unit = stemmer_porter(nlp(unit_ingredient.lower()))
        for unit_ingredient_nutrifood in ingredient_nutrifood.measures:
            if (stemmer_porter(nlp(unit_ingredient_nutrifood.name.lower())) in unit or unit in stemmer_porter(
                    nlp(unit_ingredient_nutrifood.name.lower())) or
                    unit_ingredient_nutrifood.name.lower() in unit_ingredient.lower()):
                fraction = quantity_frac(quantity_ingredient)
                return MeasuresDto(unit_ingredient_nutrifood.id, fraction[0], fraction[1], fraction[2])
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
                                 log_measures_ingredient_fails, recipe.url, _ingredient.name)
                return False
        else:
            _recipe_dto.quantities.append(QuantityDto(ingredient_nutri_.id, 0))
            return True

    def nlp_association_ingredient(_ingredient_nutri: IngredientNutri, _ingredient: IngredientIntegration,
                                   recipe_dto_: RecipeDTO):
        if _ingredient.name == "agua":
            return True
        if _ingredient_nutri is None:
            ingredient_nutri_ = search_ingredient_nutrifoods_contains(text_normalized)
            if ingredient_nutri_ is None:
                add_logs_ingredient(log_ingredient_fails, _ingredient.name, recipe.url)
                return False
            else:
                return match_unit_quantity(_ingredient, ingredient_nutri_, recipe_dto_)
        else:
            return match_unit_quantity(_ingredient, _ingredient_nutri, recipe_dto_)

    log_measures_ingredient_fails: [LogsIngredientFailsMeasure] = []
    log_ingredient_fails: [LogsIngredientFails] = []
    recipe_correct = True
    recipes_associated_with_nutrifoods: [RecipeDTO] = []
    for index, recipe in enumerate(recipes, start=1):
        recipe_dto = RecipeDTO(recipe.name_recipe, recipe.author, recipe.url, recipe.portions, recipe.preparation_time,
                               recipe.difficulty, recipe.food_days, recipe.category_recipe)
        for ingredient in recipe.ingredient_parser:
            text_normalized = unidecode(ingredient.name.lower().strip().replace(".", ""))
            ingredient_nutri: [IngredientNutri] = search_ingredient_nutrifoods(text_normalized)
            recipe_correct = nlp_association_ingredient(ingredient_nutri, ingredient, recipe_dto)
            if recipe_correct is False:
                break

        if recipe_correct:
            recipes_associated_with_nutrifoods.append(recipe_dto)

    save_logs_ingredient_fails(log_ingredient_fails)
    save_ingredient_measure_fails(log_measures_ingredient_fails)
    print(len(recipes_associated_with_nutrifoods))
    return recipes_associated_with_nutrifoods
