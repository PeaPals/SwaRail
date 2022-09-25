from ursina import Entity, Vec3
from SwaRail import constants

class Hault(Entity):
    def __init__(self, parent_track_circuit_id, **kwargs):
        super().__init__()

        self.parent_track_circuit_id = parent_track_circuit_id


    def finalize(self):
        self.finalize_attributes()
        self.draw()

        return self.color


    def draw(self):
        self.model = 'quad'
        self.color = constants.HAULT_COLOR


    def finalize_attributes(self):
        track_circuit = constants.Database.TRACK_CIRCUITS[self.parent_track_circuit_id]
        
        self.position = (track_circuit.starting_pos + track_circuit.ending_pos) / 2
        self.position += Vec3(0, 0, 0.1)

        track_circuit_length = track_circuit.ending_pos.x - track_circuit.starting_pos.x
        self.scale = Vec3(track_circuit_length, constants.HAULT_WIDTH_FROM_TRACKS, 1)

    


    def __str__(self):
        return f'''
        I Am A Hault
        parent track circuit ID = {self.parent_track_circuit_id}, color = {self.color}
        '''

    def input(self, key):
        pass

    def update(self):
        pass