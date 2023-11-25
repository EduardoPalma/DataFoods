class Measure:
    def __init__(self, id, name, grams):
        self.id = id
        self.name = name
        self.grams = grams


class IngredientNutri:
    def __init__(self, id: str, name: str, measures: list[Measure]):
        self.id = id
        self.name = name
        self.measures = measures


class IngredientIntegration:
    def __init__(self, ingredient_name, unit, quantity):
        self.name = ingredient_name
        self.unit = unit
        self.quantity = quantity


class IngredientSynonym:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.synonym = []
