from recipe.entities.IngredientNutri import IngredientNutri
from recipe.entities.Recipe import Recipe
import spacy
from unidecode import unidecode

nlp = spacy.load("es_core_news_sm")

from nltk.stem import PorterStemmer


def association_with_nutrifoods_ingredient(recipes: list[Recipe], ingredient_nutrifoods: list[IngredientNutri]):
    def search_ingredient_nutrifoods(ingredient_: str) -> IngredientNutri | None:
        for ingredient_nutrifood in ingredient_nutrifoods:
            if stemmer.stem(unidecode(ingredient_nutrifood.name.lower().strip())) == ingredient_:
                return ingredient_nutrifood
        return None

    stemmer = PorterStemmer()
    for recipe in recipes:
        for ingredient in recipe.ingredient_parser:
            #para una lista en caso de
            ingredient_stemmer = stemmer.stem(unidecode(ingredient.name.lower().strip()))
            ingredient_nutri: [IngredientNutri] = search_ingredient_nutrifoods(ingredient_stemmer)
            if ingredient_nutri is None:
                print("Eliminar Receta: ingrediente no existente", ingredient.name, " stemmer", ingredient_stemmer)
                break
            print(recipe.name_recipe)
            if ingredient.unit is not None and ingredient.unit != "":
                unit = nlp(ingredient.unit.lower().strip())[0].lemma_
                stemmed_words = stemmer.stem(ingredient.unit.lower().strip())
    # con las recetas ya empezar a asociadar cada una de ellas con los ingredientes correctos, para eso hacer la clase dto de receta con ingrediente
    # el contenido a conversar
    # para el proceso de normalizacion, se tiene que normalizar el texto, por parte del ingrediente como del ingrediente en nutrifoods
    # letas en minusculas y sin acentos
    # aplicar ademas una tecnica de lematizacion o stemming, mas a lematizacion
    # el proceso de bsuqeuda sera por coincidencia exacta, en caso que no encuentra busca si ese ingrediente dentro de nutrifoods, esta contenido dentro del texto
    # en cumple en caso que sea lechuga "nombre real" contiene lechuga y se utiliza ese.
    # por ultimo por similutd de string, esto quiere decir que tan parecido es el ingrediente con uno de ellos, la exactitud del modelo deberia del mayor a 90%
    # dependiendo de lo que se va a relizar si tiene una unidad de medida en gramos o cualquier otro tipo convertirlo a gramos, todo los demas a unidad de medida
