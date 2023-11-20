import csv


class LogsIngredientFailsMeasure:

    def __init__(self, name_ingredient, ingredient):
        self.name_ingredient = name_ingredient
        self.urls = []
        self.ingredient = ingredient
        self.name_measures = []

    def add_measure_and_url(self, name_measure, url):
        self.name_measures.append(name_measure)
        self.urls.append(url)


class LogsIngredientFails:
    def __init__(self, name_ingredient):
        self.name_ingredient = name_ingredient
        self.urls = []

    def add_url(self, url):
        self.urls.append(url)


def get_logs(resp):
    logs_id = []
    for hit in resp['hits']['hits']:
        logs_id.append(hit['_source']['id'])
    return logs_id


def save_logs_ingredient_fails(logs_ingredient_fails):
    with open("analysis/fails_ingredient_es.csv", mode='w', newline='', encoding="utf-8") as archivo_csv:
        head = ["nombre_ingredient", "urls"]
        write_csv = csv.DictWriter(archivo_csv, fieldnames=head)
        write_csv.writeheader()
        for log in logs_ingredient_fails:
            write_csv.writerow(
                {"nombre_ingredient": log.name_ingredient, "urls": ';'.join(map(str, log.urls))})


def save_ingredient_measure_fails(logs_ingredient_measure_fails):
    with open("analysis/fails_ingredient_measure.csv_es", mode='w', newline='', encoding="utf-8") as archivo_csv:
        head = ["nombre_ingrediente_nutrifoods", "name_ingrediente_encontrado", "unidades_falladas", "urls"]
        write_csv = csv.DictWriter(archivo_csv, fieldnames=head)
        write_csv.writeheader()
        for log in logs_ingredient_measure_fails:
            write_csv.writerow(
                {"nombre_ingrediente_nutrifoods": log.name_ingredient, "name_ingrediente_encontrado": log.ingredient,
                 "unidades_falladas": ';'.join(map(str, log.name_measures)), "urls": ';'.join(map(str, log.urls))})


def add_logs_measure(ingredient_nutri_, ingredient_unit,
                     log_measures_ingredient_fails_: [LogsIngredientFailsMeasure],
                     url, ingredient_):
    for log_measure in log_measures_ingredient_fails_:
        if ingredient_nutri_ == log_measure.name_ingredient:
            if ingredient_unit not in log_measure.name_measures:
                log_measure.add_measure_and_url(ingredient_unit, url)
                return
            else:
                return

    log_ingredient_fail = LogsIngredientFailsMeasure(ingredient_nutri_, ingredient_)
    log_ingredient_fail.add_measure_and_url(ingredient_unit, url)
    log_measures_ingredient_fails_.append(log_ingredient_fail)


def add_logs_ingredient(log_ingredient_fails_: [LogsIngredientFails], ingredient_name, url):
    for log_ingredient in log_ingredient_fails_:
        if log_ingredient.name_ingredient == ingredient_name:
            log_ingredient.add_url(url)
            return

    log_ingredient = LogsIngredientFails(ingredient_name)
    log_ingredient.add_url(url)
    log_ingredient_fails_.append(log_ingredient)


class Logs:
    def __init__(self, _id, _type, _date):
        self.id = _id
        self.type = _type
        self.date = _date

    def tojson(self):
        return {"id": self.id, "type": self.type, "date": self.date}
