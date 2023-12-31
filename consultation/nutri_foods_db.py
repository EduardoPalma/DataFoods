import psycopg2
from recipe.entities.ingredient_nutrifood import IngredientNutri, Measure, IngredientSynonym


def convert_object_ingredient_sy(result) -> list[IngredientSynonym]:
    return [IngredientSynonym(id, name, synonyms) for id, name, synonyms in result]


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
            if ingredient.id == id_ingredient and name_measure is not None:
                measure = Measure(id_measure_ingredient, name_measure, grams)
                ingredient.measures.append(measure)
                found = True
                break
        if not found:
            measures: list[Measure] = []
            if name_measure is not None:
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
            "SELECT i.id, i.name, im.id AS measure_id, im.name AS measure_name, im.grams "
            "FROM ingredient AS i LEFT JOIN ingredient_measure AS im"
            " ON i.id = im.ingredient_id;")
        result = cl.fetchall()
        return convert_object_ingredient(result)

    def get_ingredient_synonyms(self):
        cl = self.client.cursor()
        cl.execute("select i.id,i.name,i.synonyms from ingredient as i")
        result = cl.fetchall()
        return convert_object_ingredient_sy(result)

    def get_name_recipe_nutrifoods(self):
        cl = self.client.cursor()
        cl.execute("select r.url from recipe as r;")
        result = [url[0] for url in cl.fetchall()]
        return result
