from consultation.queries_recipe_ingredient import QueriesRecipeIngredient
from consultation.translate import Translate
from integration import transformations


def init_pipeline(size_recipes, language="es"):
    # hacer instancias de Elastic y NutrifoodDB
    queries = QueriesRecipeIngredient()
    ingredient_nutrifoods = queries.queries_ingredient_nutrifoods()
    ingredient_synonym = queries.queries_ingredient_synonym()
    if language == 'en':
        recipes = queries.recipes_english(size_recipes)
        print(len(recipes))
    else:
        recipes = queries.recipes_spanish(size_recipes)

    recipes_ = transformations.pipeline(recipes, ingredient_nutrifoods, ingredient_synonym, language, queries.client)
    print(len(recipes_))


if __name__ == '__main__':
    init_pipeline(20, "en")
