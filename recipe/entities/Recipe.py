from recipe.entities.IngredientNutri import IngredientIntegration


def convert_ingredient(resp):
    ingredients = []
    for ingredients_text in resp:
        ingredients.append(ingredients_text['ingredientText'])
    return ingredients


class Recipe:
    def __init__(self, resp):
        self.resp = resp
        self.name_recipe = resp['name']
        self.author = resp['autor']
        self.url = resp['url']
        self.id_image = resp['idImage']
        self.portions = resp['portions']
        self.preparation_time = resp['preparationTime']
        self.difficulty = resp['difficulty']
        self.category_recipe = resp['categoryRecipe']
        self.food_days = resp['foodDays']
        self.ingredients = convert_ingredient(resp['ingredients'])
        self.steps = resp['steps']
        self.ingredients_translate = []
        self.ingredient_parser: list[IngredientIntegration] = []

    def print_ingredient(self):
        for ingredient in self.ingredients:
            print(ingredient)

    @staticmethod
    def get_recipes(resp):
        recipes = []
        for hit in resp['hits']['hits']:
            recipe = Recipe(hit['_source'])
            recipes.append(recipe)
        return recipes
