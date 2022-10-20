class State:
    # states of nodes
    AVAILABLE = 0
    BOOKED = 1
    OCCUPIED = 2

    # states of trains
    RUNNING = 3
    HAULTED = 4

    # states of signals
    RED = 5
    YELLOW = 6
    GREEN = 7
    DOUBLE_YELLOW = 8


class Type:
    # types of nodes
    TRACK = 0
    INTERSECTION = 1
    ANONYMOUS = 2

    # types of trains
    PASSENGER = 3
    FREIGHT = 4

    # types of signals # TODO :- complete and use this list
    RYG = 5