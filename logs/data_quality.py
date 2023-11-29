import datetime

from consultation.elastic_search import Elastic


def duplicity(before_recipes: int, after_recipes: int):
    duplicity_ = 1 - float(after_recipes / before_recipes)
    return {
        "duplicity": duplicity_,
        "date": datetime.datetime.now()
    }


def accuracy(before_recipes: int, after_recipes: int):
    accuracy_ = float(after_recipes / before_recipes)
    return {
        "accuracy": accuracy_,
        "date": datetime.datetime.now()
    }


def logs_metrics_data_quality(client_elastic: Elastic, recipes_cleaning, recipes_original, recipes_association):
    def insert_logs_duplicity(_client_elastic: Elastic, _recipes_cleaning, _recipes_original):
        _client_elastic.insert_logs(duplicity(len(_recipes_original), len(_recipes_cleaning)), "logs-duplicity")

    def insert_logs_accuracy(_client_elastic: Elastic, _recipes_cleaning, _recipes_association):
        _client_elastic.insert_logs(accuracy(len(_recipes_cleaning), len(_recipes_association)), "logs-accuracy")

    insert_logs_duplicity(client_elastic, recipes_cleaning, recipes_original)
    insert_logs_accuracy(client_elastic, recipes_cleaning, recipes_association)
