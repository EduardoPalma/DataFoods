from consultation.QueriesRecipeIngredient import QueriesRecipeIngredient
from integration import Transformations


def init_pipeline(size_recipes, index="es"):
    queries = QueriesRecipeIngredient()
    ingredient_nutrifoods = queries.queries_ingredient_nutrifoods()
    recipes = queries.recipes_english(size_recipes)
    Transformations.pipeline(recipes,ingredient_nutrifoods)
    print(len(recipes))


if __name__ == '__main__':
    # 523 para abarcar el total de recetas en 1 semana
    init_pipeline(50, "es")
