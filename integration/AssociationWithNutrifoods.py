from recipe.entities.IngredientNutri import IngredientNutri
from recipe.entities.Recipe import Recipe
import spacy
from unidecode import unidecode
from nltk.stem import PorterStemmer

nlp = spacy.load("es_core_news_lg")


# se pueden utilizxar modeles pre entrenados mas grandes es_core_news_md o es_core_news_lg


def association_with_nutrifoods_ingredient(recipes: list[Recipe], ingredient_nutrifoods: list[IngredientNutri]):
    def search_ingredient_nutrifoods(ingredient_: str) -> IngredientNutri | None:
        for ingredient_nutrifood in ingredient_nutrifoods:
            if unidecode(ingredient_nutrifood.name.lower().strip()) == ingredient_:
                return ingredient_nutrifood
        return None

    def search_ingredient_nutrifoods_contains(ingredient_: str) -> IngredientNutri | None:
        coincidences = []
        ingredient_similarity = nlp(ingredient_)

        for ingredient_nutrifood in ingredient_nutrifoods:
            if ingredient_ in unidecode(ingredient_nutrifood.name.lower().strip()):
                ingredient_similarity_nutrifood = nlp(unidecode(ingredient_nutrifood.name.lower().strip()))
                similarity = ingredient_similarity.similarity(ingredient_similarity_nutrifood)
                coincidences.append((ingredient_nutrifood, similarity))

        if coincidences:
            max_similarity = max(coincidences, key=lambda t: t[1])
            return max_similarity[0]
        else:
            coincidences.clear()
            for ingredient_nutrifood in ingredient_nutrifoods:
                if unidecode(ingredient_nutrifood.name.lower().strip()) in ingredient_:
                    ingredient_similarity_nutrifood = nlp(unidecode(ingredient_nutrifood.name.lower().strip()))
                    similarity = ingredient_similarity_nutrifood.similarity(ingredient_similarity)
                    coincidences.append((ingredient_nutrifood, similarity))

            if coincidences:
                max_similarity = max(coincidences, key=lambda t: t[1])
                if max_similarity[1] >= 0.5:
                    return max_similarity[0]
                else:
                    return None
            else:
                return None

    # lematizador
    def stemmer_porter(doc_):
        text_stemmer = [stemmer.stem(token.text) for token in doc_]
        return " ".join(text_stemmer)

    def lematizer(doc_):
        text_lema = [token.lemma_ for token in doc_]
        return " ".join(text_lema)

    def search_ingredient_unit(ingredient_nutrifood: IngredientNutri, unit_ingredient: str):
        if unit_ingredient is None or unit_ingredient == "":
            return
        if "g" in unit_ingredient or "lb" in unit_ingredient or "ml" in unit_ingredient:
            return

        for unit_ingredient_nutrifood in ingredient_nutrifood.measures:
            if unit_ingredient_nutrifood.name.lower() in unit_ingredient.lower():
                return

    stemmer = PorterStemmer()
    cant_recipe_ok = len(recipes)
    for index, recipe in enumerate(recipes, start=1):
        for ingredient in recipe.ingredient_parser:
            text_normalized = unidecode(ingredient.name.lower().strip().replace(".", ""))
            ingredient_nutri: [IngredientNutri] = search_ingredient_nutrifoods(lematizer(nlp(text_normalized)))
            if ingredient_nutri is None and ingredient.name != "agua":
                ingredient_nutri = search_ingredient_nutrifoods_contains(text_normalized)
                if ingredient_nutri is None:
                    cant_recipe_ok -= 1
                    print("No encontro resultado ", ingredient.name, "Receta : ", recipe.url)
                    break
                else:
                    # print(ingredient.name, " ", ingredient_nutri.name)
                    search_ingredient_unit(ingredient_nutri, ingredient.unit)
                    # print(ingredient_nutri.name, " ", ingredient.name, " ", ingredient_stemmer)

            else:
                if ingredient.unit is not None and ingredient.unit != "" and ingredient.name != "agua":
                    # print(ingredient.name, " ", ingredient_nutri.name)
                    search_ingredient_unit(ingredient_nutri, ingredient.unit)
                else:
                    if ingredient.name != "agua":
                        pass
                        # print(ingredient.name, " ", ingredient_nutri.name)

    print(cant_recipe_ok)
    # con las recetas ya empezar a asociadar cada una de ellas con los ingredientes correctos, para eso hacer la clase dto de receta con ingrediente
    # el contenido a conversar
    # para el proceso de normalizacion, se tiene que normalizar el texto, por parte del ingrediente como del ingrediente en nutrifoods
    # letas en minusculas y sin acentos
    # aplicar ademas una tecnica de lematizacion o stemming, mas a lematizacion
    # el proceso de bsuqeuda sera por coincidencia exacta, en caso que no encuentra busca si ese ingrediente dentro de nutrifoods, esta contenido dentro del texto
    # en cumple en caso que sea lechuga "nombre real" contiene lechuga y se utiliza ese.
    # por ultimo por similutd de string, esto quiere decir que tan parecido es el ingrediente con uno de ellos, la exactitud del modelo deberia del mayor a 90%
    # dependiendo de lo que se va a relizar si tiene una unidad de medida en gramos o cualquier otro tipo convertirlo a gramos, todo los demas a unidad de medida
