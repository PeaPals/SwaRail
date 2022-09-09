from ursina import Entity, Mesh
from SwaRail import constants

class TrackCircuit(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.ID = None
        self.starting_pos = None
        self.ending_pos = None
        self.connections = {'right': [], 'left': []}
        self.direction = None
        self.color = None
        self.signals = {'right': [], 'left': []}
        self.hault_id = None
        self.line_length = 0
        self.track_circuit_length = 0

    def finalize(self):
        # order is important
        self.finalize_track_circuit()
        self.finalize_signals()
        self.finalize_station()


    def finalize_track_circuit(self):
        # setting attributes
        self.color = constants.TRACK_CIRCUIT_COLOR[self.direction]
        self.line_length = self.ending_pos.x - self.starting_pos.x
        self.track_circuit_length = round(self.line_length * 100) / 1000

        # TODO :- remove this
        import random
        x = random.choice(constants.colors)

        # setting model
        self.model = Mesh(
            vertices=[self.starting_pos, self.ending_pos],
            colors=[self.color, self.color],
            # colors=[x, x],
            mode='line', 
            thickness=constants.TRACK_CIRCUIT_THICKNESS
        )


    def finalize_signals(self):
        # reversing the order of left direction signals
        self.signals['left'].reverse()


    def finalize_station(self):
        if self.hault_id == None:
            return None
        
        station = constants.Database.HAULTS[self.hault_id]
        station.finalize()


    def __str__(self):
        return f'''
        ID = {self.ID}, starting pos = {self.starting_pos}, ending pos = {self.ending_pos}, length = {self.track_circuit_length} KM,
        direction = {self.direction}, connections = {self.connections}, color = {self.color}
        '''

    def input(self, key):
        pass

    def update(self):
        pass




class Track:
    pass