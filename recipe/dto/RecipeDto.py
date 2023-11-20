class RecipeDTO:
    def __init__(self, name, author, url, portions, preparation_time, difficulty, meal_types, dish_types):
        self.name: str = name
        self.author: str = author
        self.url: str = url
        self.portions: int = portions
        self.preparationTime: int = preparation_time
        self.difficulty: str = difficulty
        self.mealTypes: list[str] = meal_types
        self.dishTypes: list[str] = dish_types
        self.measures: list[MeasuresDto] = []
        self.quantities: list[QuantityDto] = []
        self.step: list[StepDto] = []

    def to_json(self):
        return {
            "name": self.name,
            "author": self.author,
            "url": self.url,
            "portions": self.portions,
            "preparationTime": self.preparationTime,
            "difficulty": self.difficulty,
            "mealTypes": self.mealTypes,
            "dishTypes": self.dishTypes,
            "measures": [measure.__json__() for measure in self.measures],
            "quantities": [quantity.__json__() for quantity in self.quantities],
            "steps": [step.__json__() for step in self.step]
        }


class MeasuresDto:
    def __init__(self, measure_id, integer_part, numerator, denominator):
        self.measureId: int = measure_id
        self.integerPart: int = integer_part
        self.numerator: int = numerator
        self.denominator: int = denominator

    def __json__(self):
        return {
            "measureId": self.measureId,
            "integerPart": self.integerPart,
            "numerator": self.numerator,
            "denominator": self.denominator
        }


class QuantityDto:
    def __init__(self, ingredient_id, grams):
        self.id: int = ingredient_id
        self.grams: float = grams

    def __json__(self):
        return {
            "id": self.id,
            "grams": self.grams
        }


class StepDto:
    def __init__(self, number, description):
        self.number = number
        self.description = description

    def __json__(self):
        return {
            "number": self.number,
            "description": self.description
        }
