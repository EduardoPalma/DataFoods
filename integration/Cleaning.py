from recipe.entities.Recipe import Recipe


def cleaning(recipes: list[Recipe]):
    def duplicate_attribute(recipe_duplicate: Recipe):
        return recipe_duplicate.name_recipe

    def missing_ingredient(recipe_: Recipe):
        for ingredient_par in recipe_.ingredient_parser:
            if ingredient_par.name is None:
                return False
        return True

    def missing_data(recipe_missing: Recipe):
        if recipe_missing.portions == 0:
            return False
        elif recipe_missing.name_recipe == '':
            return False
        elif len(recipe_missing.steps) == 0 or len(recipe_missing.ingredients) == 0:
            return False
        elif missing_ingredient(recipe_missing) is False:
            return False
        else:
            return True

    # duplicados y faltantes
    recipes_uniq = set()
    recipes_aux: list[Recipe] = []
    for recipe in recipes:
        if duplicate_attribute(recipe) not in recipes_uniq and missing_data(recipe):
            recipes_uniq.add(duplicate_attribute(recipe))
            recipes_aux.append(recipe)

    return recipes_aux
