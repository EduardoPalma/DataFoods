from consultation.QueriesRecipeIngredient import QueriesRecipeIngredient
from integration import Transformations


def init_pipeline(size_recipes, language="es"):
    #hacer instancias de Elastic y NutrifoodDB
    queries = QueriesRecipeIngredient()
    ingredient_nutrifoods = queries.queries_ingredient_nutrifoods()
    ingredient_synonym = queries.queries_ingredient_synonym()
    if language == 'en':
        recipes = queries.recipes_english(size_recipes)
    else:
        recipes = queries.recipes_spanish(size_recipes)

    recipes_ = Transformations.pipeline(recipes, ingredient_nutrifoods, ingredient_synonym, language, queries.client)
    print(len(recipes_))


if __name__ == '__main__':
    init_pipeline(1889, "en")
