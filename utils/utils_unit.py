from fractions import Fraction


def convert_unit(category_unit: str, quantity: str) -> float:
    if category_unit == "lb":
        if '/' in quantity and ' ' not in quantity:
            return float(Fraction(quantity)) * 453.592
        elif '/' in quantity and ' ' in quantity:
            integer_part = quantity.split(" ")[0]
            numerator_denominator = quantity.split(" ")[1]
            return (float(integer_part) + (float(Fraction(numerator_denominator)))) * 453.592
        else:
            return float(Fraction(quantity)) * 453.592
    elif category_unit == "oz":
        if '/' in quantity and ' ' not in quantity:
            return float(Fraction(quantity)) * 28.3495
        elif '/' in quantity and ' ' in quantity:
            integer_part = quantity.split(" ")[0]
            numerator_denominator = quantity.split(" ")[1]
            return (float(integer_part) + (float(Fraction(numerator_denominator)))) * 28.3495
        else:
            return float(quantity) * 28.3495
    elif category_unit == "kg":
        if '/' in quantity and ' ' not in quantity:
            return float(Fraction(quantity)) * 1000
        elif '/' in quantity and ' ' in quantity:
            integer_part = quantity.split(" ")[0]
            numerator_denominator = quantity.split(" ")[1]
            return (float(integer_part) + (float(Fraction(numerator_denominator)))) * 1000
        else:
            return float(quantity) * 1000


def quantity_frac(quantity: str) -> (int, int, int):
    if '/' in quantity:
        fraction = quantity.split("/")
        if len(quantity) <= 2:
            return int(quantity), 0, 0
        elif len(quantity) == 3:
            return 0, int(fraction[0]), int(fraction[1])
        else:
            if ' ' in quantity:
                return int(fraction[0].split(" ")[0]), int(fraction[0].split(" ")[1]), int(fraction[1])

            return int(fraction[0]), int(fraction[1]), int(fraction[2])
    else:
        if quantity != "half":
            return int(quantity), 0, 0
        else:
            return 0, 0, 0


def quantity_unit(unit: str, quantity_ingredient: str) -> float:
    if unit == "g":
        return float(quantity_ingredient)
    elif unit == "ml":
        return float(quantity_ingredient) * 1.85
    else:
        return convert_unit(unit, quantity_ingredient)
