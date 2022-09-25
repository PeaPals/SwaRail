from ursina import Entity, Vec3
from SwaRail import constants

class Seperator(Entity):
    def __init__(self, position, **kwargs):
        super().__init__()

        self.position = position

    def finalize(self):
        # adding little elivation to cover joints between track circuits
        # TODO :- should  keep this above or below? i.e., z -= 0.1 or z += 0.1?
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