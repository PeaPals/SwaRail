from ursina import Entity, color
from SwaRail import constants

class Signal(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.ID = None
        self.parent_track_circuit_id = None
        self.direction = None
        self.position = None
        self.signal_type = None

        self.model = 'circle'
        self.color = color.red

        if constants.SIGNAL_SIZE == None:
            self.scale = len(self.type) / 40
        else:
            self.scale = constants.SIGNAL_SIZE


    def __str__(self):
        return f'''
        ID = {self.ID}, position = {self.position}, type = {self.signal_type},
        direction = {self.direction}, parent track circuit ID = {self.parent_track_circuit_id}, color = {self.color}
        '''

    def input(self, key):
        pass

    def update(self):
        pass