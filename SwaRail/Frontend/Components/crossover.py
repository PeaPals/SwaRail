from ursina import Entity, Mesh, color
from SwaRail import constants
from SwaRail.Utilities import mathematical

class Crossover(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.ID = None
        self.connections = {'right': [], 'left': []}
        self.connecting_track_circuits = []
        self.direction = None
        self.starting_pos = None
        self.ending_pos = None
        self._is_active = False


    def update_attributes(self, track_circuit_1, track_circuit_2):
        # setting attributes
        self.line_length = mathematical.coordinate_distance(self.starting_pos, self.ending_pos, vec3=True)
        self.track_circuit_length = round(self.line_length * 100) / 1000

        self.color_1 = track_circuit_1.color
        self.color_2 = track_circuit_2.color

        # setting model
        self.model = Mesh(
            vertices=[self.starting_pos, self.ending_pos],
            colors = [self.color_1, self.color_2],
            mode='line', 
            thickness=constants.TRACK_CIRCUIT_THICKNESS
        )

    def finalize_crossover(self):
        track_circuit_1_id = self.connecting_track_circuits[0]
        track_circuit_2_id = self.connecting_track_circuits[1]

        track_circuit_1 = constants.Database.TRACK_CIRCUITS[track_circuit_1_id]
        track_circuit_2 = constants.Database.TRACK_CIRCUITS[track_circuit_2_id]

        self.update_attributes(track_circuit_1, track_circuit_2)
        self.set_to_main_line()


    def set_to_main_line(self):
        # TODO :- add feature to blink for 2 seconds before changing (use Entity.blink())
        if self._is_active == False:
            return None

        self.toggle_crossover()

    
    def set_to_change_lines(self):
        # TODO :- add feature to blink for 2 seconds before changing (use Entity.blink())
        if self._is_active == True:
            return None

        self.toggle_crossover()


    def toggle_crossover(self):
        if self._is_active == True:
            self._is_active = False
            
            self.model = Mesh(
                vertices=[self.starting_pos, self.ending_pos],
                colors = [constants.CROSSOVER_INACTIVE_COLOR, constants.CROSSOVER_INACTIVE_COLOR],
                mode='line', 
                thickness=constants.TRACK_CIRCUIT_THICKNESS
            )

        else:
            self._is_active = True

            self.model = Mesh(
                vertices=[self.starting_pos, self.ending_pos],
                colors = [self.color_1, self.color_2],
                mode='line', 
                thickness=constants.TRACK_CIRCUIT_THICKNESS
            )



    def __str__(self):
        return f'''
        ID = {self.ID}, connecting track circuits = {self.connecting_track_circuits},
        direction = {self.direction}, connections = {self.connections}
        '''

    def input(self, key):
        pass

    def update(self):
        pass