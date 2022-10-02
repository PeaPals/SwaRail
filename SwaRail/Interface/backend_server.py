from SwaRail.Server import train_handler

def get_route_from_server(train_number):
    return train_handler.get_train_route(train_number)