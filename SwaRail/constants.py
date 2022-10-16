class State:
    # states of nodes
    AVAILABLE = 0
    BOOKED = 1
    OCCUPIED = 2

    # states of trains
    RUNNING = 3
    STANDING = 4


class Type:
    # types of nodes
    TRACK = 0
    INTERSECTION = 1
    ANONYMOUS = 2

    # types of trains
    PASSENGER = 3
    FREIGHT = 4