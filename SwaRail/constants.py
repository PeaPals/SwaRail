class State:
    # states of nodes
    AVAILABLE = 0
    BOOKED = 1
    OCCUPIED = 2
    DEACTIVE = 3

    # states of trains
    RUNNING = 4
    HAULTED = 5

    # states of signals
    RED = 6
    YELLOW = 7
    GREEN = 8
    DOUBLE_YELLOW = 9


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