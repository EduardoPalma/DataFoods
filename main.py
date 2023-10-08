from consultation.QueriesRecipeIngredient import QueriesRecipeIngredient


def init_pipeline(size_recipes, index="es"):
    queries = QueriesRecipeIngredient()
    result = queries.queries_ingredient_nutrifoods()
    print(len(result))
    for ingredient in result:
        print(ingredient.id, " ", ingredient.name)
        for measure in ingredient.measures:
            print("    ", measure.id, " ", measure.name, " ", measure.grams)

    if index == "en":
        recipes = queries.recipes_english(size_recipes)
    else:
        recipes = queries.recipes_spanish(size_recipes)

    print(recipes)



if __name__ == '__main__':
    # 523 para abarcar el total de recetas en 1 semana
    init_pipeline(10, "es")
