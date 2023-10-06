from consultation.RecipeQueries import RecipeQueries


def init_pipeline(size_recipes, index="es"):
    recipes_queries = RecipeQueries()
    if index == "en":
        recipes = recipes_queries.recipes_english(size_recipes)
    else:
        recipes = recipes_queries.recipes_spanish(size_recipes)
    for recipe in recipes:
        print(recipe.name_recipe)


if __name__ == '__main__':
    # 523 para abarcar el total de recetas en 1 semana
    init_pipeline(10, "es")
