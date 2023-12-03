class RecipeDTO:
    def __init__(self, name, author, url, portions, preparation_time, difficulty, meal_types, dish_types, steps):
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
        self.steps: list[str] = steps

    def to_json(self):
        if self.preparationTime == 0:
            self.preparationTime = None

        if self.difficulty == '' or self.difficulty is None:
            return {
                "name": self.name,
                "author": self.author,
                "url": self.url,
                "portions": self.portions,
                "preparationTime": self.preparationTime,
                "difficulty": None,
                "mealTypes": self.mealTypes,
                "dishTypes": self.dishTypes,
                "measures": [measure.__json__() for measure in self.measures],
                "quantities": [quantity.__json__() for quantity in self.quantities],
                "steps": self.steps
            }
        else:
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
                "steps": self.steps
            }


class MeasuresDto:
    def __init__(self, name, ingredient_name, integer_part, numerator, denominator):
        self.name: str = name
        self.ingredientName: str = ingredient_name
        self.integerPart: int = integer_part
        self.numerator: int = numerator
        self.denominator: int = denominator

    def __json__(self):
        return {
            "name": self.name,
            "ingredientName": self.ingredientName,
            "integerPart": self.integerPart,
            "numerator": self.numerator,
            "denominator": self.denominator
        }


class QuantityDto:
    def __init__(self, ingredient_name, grams):
        self.ingredientName: int = ingredient_name
        self.grams: float = grams

    def __json__(self):
        return {
            "ingredientName": self.ingredientName,
            "grams": self.grams
        }
