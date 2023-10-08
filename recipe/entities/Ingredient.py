class Measure:
    def __init__(self, id, name, grams):
        self.id = id
        self.name = name
        self.grams = grams


class Ingredient:
    def __init__(self, id: str, name: str, measures: list[Measure]):
        self.id = id
        self.name = name
        self.measures = measures
