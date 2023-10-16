import psycopg2

from recipe.entities.IngredientNutri import IngredientNutri, Measure, IngredientSynonym


def convert_object_ingredient_sy(result) -> list[IngredientSynonym]:
    ingredients_values = {}
    for id, name, synonym in result:
        if id not in ingredients_values:
            ingredients_values[id] = IngredientSynonym(id, name)
        ingredients_values[id].synonym.append(synonym)

    ingredients = list(ingredients_values.values())
    return ingredients


def convert_object_ingredient(result) -> list[IngredientNutri]:
    ingredients: list[IngredientNutri] = []
    for row in result:
        id_ingredient: str = row[0]
        name = row[1]
        id_measure_ingredient = row[2]
        name_measure = row[3]
        grams = row[4]
        found = False
        for ingredient in ingredients:
            if ingredient.id == id_ingredient:
                measure = Measure(id_measure_ingredient, name_measure, grams)
                ingredient.measures.append(measure)
                found = True
                break
        if not found:
            measures: list[Measure] = []
            measure = Measure(id_measure_ingredient, name_measure, grams)
            measures.append(measure)
            ingredient = IngredientNutri(id_ingredient, name, measures)
            ingredients.append(ingredient)
    return ingredients


class NutrifoodDB:
    def __init__(self, db_name, user, pw, host, port):
        self.db_name = db_name
        self.user = user
        self.pw = pw
        self.host = host
        self.port = port
        self.client = self.connect()

    def connect(self):
        param = {'dbname': self.db_name,
                 'user': self.user,
                 'password': self.pw,
                 'host': self.host,
                 'port': self.port,
                 'options': f'-c search_path=nutrifoods'}
        try:
            conn = psycopg2.connect(**param)
            return conn
        except Exception as error:
            print("Error al conectarse a la base de datos:", error)

    def get_ingredient_measure(self):
        cl = self.client.cursor()
        cl.execute(
            "select i.id,i.name,im.id,im.name,im.grams from ingredient as i, ingredient_measure as im "
            "where i.id = im.ingredient_id;")
        result = cl.fetchall()
        return convert_object_ingredient(result)

    def get_ingredient_synonyms(self):
        cl = self.client.cursor()
        cl.execute(
            "select i.id,i.name,isy.name from ingredient as i, ingredient_synonym as isy"
            " where i.id = isy.ingredient_id;")
        result = cl.fetchall()
        return convert_object_ingredient_sy(result)
