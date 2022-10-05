from ursina import Entity, Vec3
from SwaRail import constants

class Seperator(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.ID = None
        self.position = None

        for key, value in kwargs.items():
            self.__setattr__(key, value)


    def finalize(self):
        self.position.z += 0.1
        self.draw()


    def draw(self):
        self.model = 'quad'
        self.color = constants.SEPERATOR_COLOR
        self.scale = Vec3(constants.SEPERATOR_SCALE)


    def __str__(self):
        return f'''
        I Am A Track Circuit Seperator
        position = {self.position}, color = {self.color}, scale = {self.scale}
        '''

    def input(self, key):
        pass

    def update(self):
        pass