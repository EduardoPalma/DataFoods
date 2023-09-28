from consultation.RecipeQueries import RecipeQueries

if __name__ == '__main__':
    recipes_queries = RecipeQueries()
    recipes = recipes_queries.recipes_english(10)
    for recipe in recipes:
        print(recipe.ingredients)
        print(recipe.ingredients_translate)
    #elastic = Elastic("localhost", "9200", "GSc_a89P7pd*6*m6Q0oF")
    #recipes_es = elastic.get_recipe_es(10)
    #recipes_en = elastic.get_recipe_en(10)

    #ingredients = recipes_es.__getitem__(1).ingredients.__getitem__(1)
    #ingredient_translate_google = Translate.translate_google(ingredients, "en")
    #ingredient_translate_memory = Translate.translate_memory(ingredients,
     ##                                                        "en-US")
    #ingredient_translate_libre = Translate.translate_libre_translate(ingredients, "en", "es")
    #try:
        #ingredient_translate_gpt = Translate.translate_gpt(ingredients, "en")
    #except:
        #print("error tranlsate GPT")

