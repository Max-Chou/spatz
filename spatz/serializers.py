import json

class JSONSerializer():
    def dumps(self, obj):
        return json.dumps(obj, seperator=(',', ':'))

    def loads(self, data):
        return json.loads(data)
