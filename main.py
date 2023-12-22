from consultation.queries_recipe_ingredient import QueriesRecipeIngredient
from integration import transformations


def init_pipeline(size_recipes, language="es"):
    queries = QueriesRecipeIngredient()
    ingredient_nutrifoods = queries.queries_ingredient_nutrifoods()
    ingredient_synonym = queries.queries_ingredient_synonym()
    urls_recipe = queries.queries_recipe_url()
    if language == 'en':
        recipes = queries.recipes_english(size_recipes)
    else:
        recipes = queries.recipes_spanish(size_recipes)

    transformations.pipeline(recipes, ingredient_nutrifoods, ingredient_synonym, language, queries.client,
                             urls_recipe)


if __name__ == '__main__':
    # Recetas en = 1894,  es = 1774
    init_pipeline(1774, "es")
