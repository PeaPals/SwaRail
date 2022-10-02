from SwaRail.database import Database
from SwaRail.Backend.path_finder import PathFinder, RouteProcessor
from SwaRail.Interface.backend_server import get_route_from_server

def book_route(train_number):
    route = get_route_from_server(train_number)
    # print(route)
    route = RouteProcessor.process_route(route)
    path = PathFinder.find_path(route[0], route[1])

    if not path:
        return []

    _book_path(path)


def _book_path(path): 
    path_colour = Database.get_next_train_color()

    for track_circuit_id in path:
        track_circuit = Database.get_component(track_circuit_id)
        track_circuit.book(color = path_colour)


def generate_signals(path):
    return []