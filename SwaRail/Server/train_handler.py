from SwaRail.Server.database import Database

def get_train_route(train_number):
    return Database.get_train_route(train_number)