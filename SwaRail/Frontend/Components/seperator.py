from ursina import Entity, Vec3
from SwaRail import constants

class Seperator(Entity):
    def __init__(self, position, **kwargs):
        super().__init__()

        self.model = 'quad'
        self.color = constants.SEPERATOR_COLOR
        self.scale = Vec3(constants.SEPERATOR_SCALE)
        self.position = position
        
        # adding little elivation to cover joints between track circuits
        self.position.z -= 0.1


    def __str__(self):
        return f'''
        I Am A Track Circuit Seperator
        position = {self.position}, color = {self.color}, scale = {self.scale}
        '''

    def input(self, key):
        pass

    def update(self):
        pass