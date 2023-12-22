import csv
import datetime
from consultation.elastic_search import Elastic


class LogsIngredientFailsMeasure:

    def __init__(self, name_ingredient, ingredient, date, language):
        self.name_ingredient = name_ingredient
        self.urls = []
        self.ingredient = ingredient
        self.name_measures = []
        self.date_time = date
        self.language = language

    def add_measure_and_url(self, name_measure, url):
        self.name_measures.append(name_measure)
        self.urls.append(url)

    def tojson(self):
        return {
            "name_ingredient_nutrifood": self.name_ingredient,
            "urls": self.urls,
            "name_ingredient_detected": self.ingredient,
            "measures_fails": self.name_measures,
            "date": self.date_time,
            "language": self.language
        }


class LogsIngredientFails:
    def __init__(self, name_ingredient, date, language):
        self.name_ingredient = name_ingredient
        self.urls = []
        self.date = date
        self.language = language

    def add_url(self, url):
        self.urls.append(url)

    def tojson(self):
        return {
            "name_ingredient": self.name_ingredient,
            "urls": self.urls,
            "date": self.date,
            "language": self.language
        }


def get_logs_recipes(resp, language: str):
    logs_id = []
    for hit in resp['hits']['hits']:
        if hit['_source']["language"] == language:
            logs_id.append(hit['_source']['nameRecipe'])
    return logs_id


def save_logs_ingredient_fails(logs_ingredient_fails: [LogsIngredientFails], client_elastic: Elastic):
    with open("analysis/fails_ingredient.csv", mode='w', newline='', encoding="utf-8") as archivo_csv:
        head = ["nombre_ingredient", "urls"]
        write_csv = csv.DictWriter(archivo_csv, fieldnames=head)
        write_csv.writeheader()
        for log in logs_ingredient_fails:
            client_elastic.insert_logs(log.tojson(), "logs-ingredient")
            write_csv.writerow(
                {"nombre_ingredient": log.name_ingredient, "urls": ';'.join(map(str, log.urls))})


def save_logs_ingredient_measure_fails(logs_ingredient_measure_fails: [LogsIngredientFailsMeasure],
                                       client_elastic: Elastic):
    with open("analysis/fails_ingredient_measure.csv", mode='w', newline='', encoding="utf-8") as archivo_csv:
        head = ["nombre_ingrediente_nutrifoods", "name_ingrediente_encontrado", "unidades_falladas", "urls"]
        write_csv = csv.DictWriter(archivo_csv, fieldnames=head)
        write_csv.writeheader()
        for log in logs_ingredient_measure_fails:
            client_elastic.insert_logs(log.tojson(), "logs-measures")
            write_csv.writerow(
                {"nombre_ingrediente_nutrifoods": log.name_ingredient, "name_ingrediente_encontrado": log.ingredient,
                 "unidades_falladas": ';'.join(map(str, log.name_measures)), "urls": ';'.join(map(str, log.urls))})


def add_logs_measure(ingredient_nutri_, ingredient_unit,
                     log_measures_ingredient_fails_: [LogsIngredientFailsMeasure],
                     url, ingredient_, language: str):
    for log_measure in log_measures_ingredient_fails_:
        if ingredient_nutri_ == log_measure.name_ingredient:
            if ingredient_unit not in log_measure.name_measures:
                log_measure.add_measure_and_url(ingredient_unit, url)
                return
            else:
                return

    log_ingredient_fail = LogsIngredientFailsMeasure(ingredient_nutri_, ingredient_, datetime.datetime.now(), language)
    log_ingredient_fail.add_measure_and_url(ingredient_unit, url)
    log_measures_ingredient_fails_.append(log_ingredient_fail)


def add_logs_ingredient(log_ingredient_fails_: [LogsIngredientFails], ingredient_name, url, language: str):
    for log_ingredient in log_ingredient_fails_:
        if log_ingredient.name_ingredient == ingredient_name:
            log_ingredient.add_url(url)
            return

    log_ingredient = LogsIngredientFails(ingredient_name, datetime.datetime.now(), language)
    log_ingredient.add_url(url)
    log_ingredient_fails_.append(log_ingredient)


def save_logs_recipes(ids: [(str, str)], language: str, client_elastic: Elastic):
    try:
        try:
            with open("analysis/id_image_recipe.csv", mode='r', encoding="utf-8") as archivo_csv:
                existing_data = list(csv.DictReader(archivo_csv))
        except FileNotFoundError:
            existing_data = []

        new_data = [{"id_image": log[0], "name_recipe": log[1]} for log in ids]
        csv_data = existing_data + new_data

        with open("analysis/id_image_recipe.csv", mode='w', newline='', encoding="utf-8") as archivo_csv:
            head = ["id_image", "name_recipe"]
            write_csv = csv.DictWriter(archivo_csv, fieldnames=head)
            write_csv.writeheader()
            write_csv.writerows(csv_data)

        for log in ids:
            client_elastic.insert_logs_recipes({"nameRecipe": log[1], "idImage": log[0], "language": language},
                                               "logs-recipe")
    except Exception as e:
        print(f"Error al agregar datos al archivo CSV: {str(e)}")
