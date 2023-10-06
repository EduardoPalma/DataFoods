def get_logs(resp):
    logs_id = []
    for hit in resp['hits']['hits']:
        logs_id.append(hit['_source']['id'])
    return logs_id


class Logs:
    def __init__(self, _id, _type, _date):
        self.id = _id
        self.type = _type
        self.date = _date

    def tojson(self):
        return {"id": self.id, "type": self.type, "date": self.date}
