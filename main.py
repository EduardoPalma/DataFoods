from consultation.QueriesRecipeIngredient import QueriesRecipeIngredient
from integration import Transformations


def init_pipeline(size_recipes, language="es"):
    queries = QueriesRecipeIngredient()
    ingredient_nutrifoods = queries.queries_ingredient_nutrifoods()
    ingredient_synonym = queries.queries_ingredient_synonym()
    if language == 'en':
        recipes = queries.recipes_english(size_recipes)
    else:
        recipes = queries.recipes_spanish(size_recipes)

    Transformations.pipeline(recipes, ingredient_nutrifoods, ingredient_synonym, language)
    print(len(recipes))


if __name__ == '__main__':
    # 523 para abarcar el total de recetas en 1 semana
    init_pipeline(10, "en")
