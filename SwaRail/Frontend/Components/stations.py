from ursina import Entity, Vec3
from SwaRail.Frontend import constants
from SwaRail.database import Database


class Hault(Entity):
    def __init__(self, starting_pos, ending_pos, **kwargs):
        super().__init__()

        self.starting_pos = starting_pos
        self.ending_pos = ending_pos

        for key, value in kwargs.items():
            self.__setattr__(key, value)


    def finalize(self):
        self.finalize_attributes()
        self.draw()

        return self.color


    def draw(self):
        self.model = 'quad'
        self.color = constants.HAULT_COLOR

    def set_color(self, color):
        self.color = color


    def finalize_attributes(self):
        
        self.position = (self.starting_pos + self.ending_pos) / 2
        self.position += Vec3(0, 0, 0.1)

        track_circuit_length = self.ending_pos.x - self.starting_pos.x
        self.scale = Vec3(track_circuit_length, constants.HAULT_WIDTH_FROM_TRACKS, 1)

    


    def __str__(self):
        return f'''
        I Am A Hault
        ID = {self.ID}, parent track circuit ID = {self.parent_track_circuit_id}, color = {self.color}
        '''

    def input(self, key):
        pass

    def update(self):
        pass