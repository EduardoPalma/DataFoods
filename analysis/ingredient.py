import pandas as pd
import csv


class Ingredient:
    def __init__(self, ids, name, id_food_data_central):
        self.ids = ids
        self.name = name
        self.id_food_data_central = id_food_data_central


def repeated_ingredient_ids():
    data_frame = pd.read_csv("analysis/ingredientIds.csv", delimiter=";")
    id_repeated = {}
    for index, row in data_frame.iterrows():
        id_food_data = row.iloc[2]
        name_ingredient = row.iloc[1]

        if id_food_data in id_repeated:
            id_repeated[id_food_data].append(name_ingredient)
        else:
            id_repeated[id_food_data] = [name_ingredient]

    with open("analysis/ingredient_id_repeated.csv", mode="w", newline="") as file:
        write_csv = csv.writer(file)
        write_csv.writerow(["id_api", "nombres_asociados"])
        for id_api, names in id_repeated.items():
            if len(names) > 1:
                write_csv.writerow([id_api, ";".join(names)])


def new_ingredient_ids():
    data_frame = pd.read_csv("analysis/ingredientIds.csv", delimiter=";", header=None)
    with open("analysis/ingredient_id_new.csv", mode="w", newline="") as file:
        write_csv = csv.writer(file)
        write_csv.writerow(["id", "name_ingredient", "id_foodData"])
        cont = 1
        for index, row in data_frame.iterrows():
            id_food_data = row.iloc[2]
            name_ingredient = row.iloc[1]
            write_csv.writerow([cont, name_ingredient, id_food_data])
            cont = cont + 1
