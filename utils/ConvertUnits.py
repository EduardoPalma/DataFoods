def convert_unit(category_unit: str, quantity: float) -> float:
    if category_unit == "lb":
        return quantity * 453.592
    elif category_unit == "oz":
        return quantity * 28.3495
    elif category_unit == "kg":
        return quantity * 1000
