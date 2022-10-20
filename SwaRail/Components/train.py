from SwaRail import State, settings
import logging

class Train:
    def __init__(self, **kwargs):
        self.number = None
        self.priority = None    # TODO :- implement priority
        self.direction = '>'
        self.state = State.RUNNING
        self.route = None
        self.path = []
        self.signal_seq = None
        self.time = None
        self.speed = None
        self.__currently_at = None

        for key, value in kwargs.items():
            setattr(self, key, value)



    @property
    def currently_at(self):
        return self.__currently_at


    @currently_at.setter
    def currently_at(self, new_position: str):
        self.__currently_at = new_position

        if self.path == []:
            return None
        
        if new_position == self.path[0]:
            self.path.pop(0)

        if new_position == self.route[0][0]:
            self.state = State.HAULTED
            self.is_haulted()
            self.update_route()
            self.timer = settings.TRAIN_HAULT_COUNT_DOWN


    def update_route(self):
        # self.route.pop(0)

        if len(self.route) == 1:
            self.route = []
            return None


        self.route = [[self.__currently_at]] + self.route[1:]



    def is_haulted(self):
        logging.info(f"Train with number : {self.number} is successfully haulted at {self.__currently_at}")