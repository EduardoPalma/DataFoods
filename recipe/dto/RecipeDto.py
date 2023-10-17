class RecipeDTO:
    def __init__(self, id, name, author, url, portions, preparation_time, difficulty):
        self.name: str = name
        self.author: str = author
        self.url: str = url
        self.portions: int = portions
        self.preparationTime: int = preparation_time
        self.difficulty: str = difficulty
        self.mealTypes: list[str] = []
        self.dishTypes: list[str] = []
        self.measures: list[MeasuresDto] = []
        self.quantities: list[QuantityDto] = []
        self.step: list[StepDto] = []


class MeasuresDto:
    def __init__(self, measure_id, integer_part, numerator, denominator):
        self.measureId: int = measure_id
        self.integerPart: int = integer_part
        self.numerator: int = numerator
        self.denominator: int = denominator


class QuantityDto:
    def __init__(self, id, grams):
        self.id: int = id
        self.grams = grams


class StepDto:
    def __init__(self, number, description):
        self.number = number
        self.description = description
