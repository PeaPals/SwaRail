from ursina import Entity, Mesh, Vec3, Text
from SwaRail import constants
from SwaRail.Utilities import mathematical

class Crossover(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.ID = None
        self.connections = {'<': [], '>': []}
        self.connecting_track_circuits = []
        self.crossover_type = None
        self.starting_pos = None
        self.ending_pos = None
        self.direction = None
        self.label = None

        self._is_active = False

        for key, value in kwargs.items():
            self.__setattr__(key, value)


    def finalize(self):
        # order is important
        self.check_crossover_validity()
        self.finalize_attributes()
        self.draw()


    def draw(self):
        # drawing the model
        self.model = Mesh(
            vertices=[self.starting_pos, self.ending_pos],
            colors = [self.color_1, self.color_2],
            mode='line', 
            thickness=constants.TRACK_CIRCUIT_THICKNESS
        )


    def finalize_attributes(self):
        # setting length of crossover attributes
        # TODO :- is it even required?
        self.length = mathematical.coordinate_distance(self.starting_pos, self.ending_pos, vec3=True)

        # setting color of crossover
        match constants.CROSSOVER_ACTIVE_COLOR:
            case None:
                track_circuit_1, track_circuit_2 = self._get_connecting_track_circuits()
                self.color_1, self.color_2 = track_circuit_1.color, track_circuit_2.color
            case _:
                self.color_1, self.color_2 = constants.CROSSOVER_ACTIVE_COLOR, constants.CROSSOVER_ACTIVE_COLOR



    def _get_connecting_track_circuits(self):
        track_circuit_1_id, track_circuit_2_id = self.connecting_track_circuits

        track_circuit_1 = constants.Database.TRACK_CIRCUITS[track_circuit_1_id]
        track_circuit_2 = constants.Database.TRACK_CIRCUITS[track_circuit_2_id]

        return track_circuit_1, track_circuit_2



    def check_crossover_validity(self):
        if self.connections['>'] == self.connections['<'] == []:
            constants.logging.critical(
                f'''The Crossover of type {self.crossover_type} starting at LINE:{int(self.starting_pos.y) + 1} COL:{int(self.starting_pos.x) + 1},
                    ending at LINE:{int(self.ending_pos.y) + 1} COL:{int(self.ending_pos.x) + 1}, doesn't align with
                    directions of its connections from both ends, thus it is consider of no particular use on map
                    and should be removed or fixed
                '''
            )


    def set_to_main_line(self):
        # TODO :- add feature to blink for 2 seconds before changing (use Entity.blink())
        pass

    
    def set_to_change_lines(self):
        # TODO :- add feature to blink for 2 seconds before changing (use Entity.blink())
        pass




    def _get_label_position(self):
        position = (self.starting_pos + self.ending_pos) / 2
        return position + constants.CROSSOVER_BASE_OFFSET


    def _get_label_rotation(self):
        rotation = constants.CROSSOVER_BASE_ROTATION

        match self.crossover_type:
            case '/': rotation *= -1

        return rotation


    def _create_label(self):
        
        self.label = Text(
            text = self.ID,
            parent = Entity(),
            color = constants.CROSSOVER_LABEL_COLOR,
            scale = constants.CROSSOVER_LABEL_SIZE,
            position = self._get_label_position(),
            rotation = self._get_label_rotation(),
        )


    def show_label(self):
        if self.label == None:
            self._create_label()

        self.label.visible = True


    def __str__(self):
        return f'''
        I Am A Crossover
        ID = {self.ID}, type = {self.crossover_type}, starting_pos = {self.starting_pos},
        ending_pos = {self.ending_pos}, connections = {self.connections}, connecting track circuits = {self.connecting_track_circuits}
        '''

    def input(self, key):
        pass

    def update(self):
        pass