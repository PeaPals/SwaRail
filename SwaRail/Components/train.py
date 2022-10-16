from SwaRail.constants import State

class Train:
    def __init__(self, **kwargs):
        self.number = None
        self.priority = None
        self.state = State.RUNNING
        self.route = None

        for key, value in kwargs.items():
            setattr(self, key, value)