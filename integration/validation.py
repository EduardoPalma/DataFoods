from recipe.dto.recipe_dto import RecipeDTO


def validation_recipe(recipes: [RecipeDTO]):
    for recipe in recipes:
        print(recipe)
