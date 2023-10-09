from recipe.dto.RecipeDto import RecipeDTO
from recipe.entities import Recipe


class Integration:
    def __init__(self, recipes: list[Recipe]):
        self.recipes = recipes

    def start(self) -> list[RecipeDTO]:
        recipes_dto: list[RecipeDTO] = []
        return recipes_dto