from ingredient_parser import parse_ingredient
from recipe.entities.Recipe import Recipe
import nltk

nltk.download('averaged_perceptron_tagger')


def acquisition_ing_unit_quantity(text: str):
    parser = parse_ingredient(text)
    ingredient = parser.name.text
    quantity = parser.amount[0].quantity
    unit = parser.amount[0].unit
    return ingredient, quantity, unit


def clean_date(recipes: list[Recipe]):

    return recipes
    # limpiar datos
    # duplicados en la lista
    # reemplazar valores, valores raros dentro de la traduccion, como traducirlar a el languaje español
    # datos faltantee
    # se tiene que desglozar en mas funciones especificas

def normalization(recipes: list[Recipe]):
    #proceso de normalizacion
    #nombres de ingredientes con pertenencia en la base de datos de nutrifoods, sinonimous
    #normliazcion de las categorias
    #y tecnica de stemming o similutd de string para busqueda o asociacion de nombres
    return recipes

def association_with_nutrifoods_ingredient(recipes: list[Recipe]):
    #se asocia y se busca los nombres de los ingredientes con la id correspondientes
    #ya sea el ingrediente con su id y la unidad de medida especifica
    return
def busines_rules(recipes: list[Recipe]):
    #reglas de negocio asociada al constexto
    #reglas todavia no definidas
    return recipes