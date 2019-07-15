import logging

class Database():
    __databases = {}

    def __init__(self, database_name=None):
        self.logger = logging.getLogger('logger')
        if database_name not in self.__databases:
            self.__databases[database_name] = []

        self.database = self.__databases[database_name]

    def delete_object(self, obj):
        self.database = [x for x in self.database if x.get('prepid') != obj.get('prepid')]

    def get_object_count(self):
        return len(self.database)

    def get(self, object_id):
        for item in self.database:
            if item.get('prepid') == object_id:
                return item
        else:
            return None

    def save(self, obj):
        object_json = obj.json()
        object_prepid = obj.get('prepid')
        if not object_prepid:
            raise Exception('Object does not have PrepID. %s' % (object_json))

        object_json['_id'] = object_prepid
        if self.get(object_prepid):
            self.delete_object(obj)

        self.database.append(object_json)
