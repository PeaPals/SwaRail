import orjson as json

class Database:
    train_routes = {}

    @classmethod
    def initialize_database(cls):
        cls.train_routes = json.loads(open('Data/Trains/route_data.json', 'rb').read())

    @classmethod
    def get_train_route(cls, train_number):
        return cls.train_routes.get(train_number, [])


Database.initialize_database()