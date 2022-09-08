from ursina import Entity, Vec3
from SwaRail import constants

class Station(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.ID = None
        self.parent_track_circuit_id = None
        self.main_station_id = None

        self.model = 'quad'
        self.color = constants.HAULT_COLOR


    def finalize(self):
        track_circuit = constants.Database.TRACK_CIRCUITS[self.parent_track_circuit_id]

        self.position = (track_circuit.starting_pos + track_circuit.ending_pos) / 2
        self.position += Vec3(0, 0, 0.1)
        
        self.scale = Vec3(track_circuit.line_length, constants.HAULT_WIDTH_FROM_TRACKS, 1)


    def __str__(self):
        return f'''
        ID = {self.ID}, position = {self.position}, main station id = {self.main_station_id},
        parent track circuit ID = {self.parent_track_circuit_id}, color = {self.color}
        '''

    def input(self, key):
        pass

    def update(self):
        pass