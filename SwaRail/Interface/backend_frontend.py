from SwaRail.database import Database
from SwaRail.Backend.path_finder import PathFinder, RouteProcessor
from SwaRail.Interface.backend_server import get_route_from_server


def path_generator(route):
    i = 0

    while i < len(route):
        path, direction = PathFinder.find_path(route[i-1], route[i])

        match len(path):
            case 0: yield False
            case _:
                _book_path(path, direction)
                i += 1
                yield True


def book_route(train_number):
    route = get_route_from_server(train_number)
    route = RouteProcessor.process_route(route)
    return path_generator(route)


def _book_path(path, direction): 
    path_color = Database.get_next_train_color()
    __book_track_circuits(path, path_color)
    __book_signals(path, direction)


def __book_track_circuits(path, path_color):
    for track_circuit_id in path:
        track_circuit = Database.get_component(track_circuit_id)
        track_circuit.book(color=path_color)


def __book_signals(path, direction):
    # TODO :- take care of partial signal booking... use indexing just like we did in postparser
    # to find out from where signals should be booked
    
    signal_sequence = []

    for track_circuit_id in path:
        if track_circuit_id[:2] == 'CO':
            continue

        track_circuit = Database.get_component(track_circuit_id)

        for signal_id in track_circuit.signals[direction]:
            signal = Database.get_component(signal_id)
            signal_sequence.append(signal)
            signal.set_signal('G')


    # TODO :- dont do manually
    signal_sequence[-4].set_signal('Y')
    signal_sequence[-3].set_signal('Y')
    signal_sequence[-2].set_signal('Y')
    signal_sequence[-1].set_signal('R')