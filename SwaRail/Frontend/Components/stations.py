from ursina import Entity, Vec3
from SwaRail import constants


class Hault(Entity):
    def __init__(self, parent_id, starting_pos, ending_pos, **kwargs):
        super().__init__()

        self.parent_tc_id : str = parent_id
        self.starting_pos = starting_pos
        self.ending_pos = ending_pos

        for key, value in kwargs.items():
            self.__setattr__(key, value)


    def finalize(self):
        self.finalize_attributes()
        self.draw()


    def draw(self):
        self.model = 'quad'
        self.set_initial_color()


    def set_initial_color(self):
        for ending_code in constants.HAULT_COLOR.keys():
            if self.parent_tc_id.endswith(ending_code):
                self.set_color(constants.HAULT_COLOR[ending_code])
                return None

        self.set_color(constants.DEFAULT_HAULT_COLOR)


    def set_color(self, color):
        self.color = color


    def finalize_attributes(self):        
        self.position = (self.starting_pos + self.ending_pos) / 2
        self.position += constants.HAULT_OFFSET

        track_circuit_length = self.ending_pos.x - self.starting_pos.x
        self.scale = Vec3(track_circuit_length, constants.HAULT_WIDTH_FROM_TRACKS, 1)


    def __str__(self):
        return f'''
        I Am A Hault
        color = {self.color}
        '''

    def input(self, key):
        pass

    def update(self):
        pass