from ursina import Entity, color
from SwaRail import constants
from SwaRail.database import State

class Signal(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.ID = None
        self.parent_track_circuit_id = None
        self.direction = None
        self.position = None
        self.signal_type = None
        self.state = State.AVAILABLE

        for key, value in kwargs.items():
            self.__setattr__(key, value)


    def finalize(self):
        self.draw()


    def draw(self):
        self.model = 'circle'
        self.color = color.red
        self.scale = constants.SIGNAL_SIZE


    def set_signal(self, signal_type):
        # TODO :- configure this with the signal type (very Important)

        match signal_type:
            case 'R': self.__set_color(color.red)
            case 'Y': self.__set_color(color.yellow)
            case 'G': self.__set_color(color.green)


    def __set_color(self, color):
        self.color = color


    def __str__(self):
        return f'''
        I Am A Signal
        ID = {self.ID}, position = {self.position}, type = {self.signal_type},
        direction = {self.direction}, parent track circuit ID = {self.parent_track_circuit_id}, color = {self.color}
        '''

    def input(self, key):
        pass

    def update(self):
        pass