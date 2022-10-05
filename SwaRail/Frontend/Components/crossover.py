from ursina import Entity, Mesh, Text
from SwaRail import constants
from SwaRail.Utilities import mathematical
from SwaRail.database import Database, State

class Crossover(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.ID = None
        self.starting_pos = None
        self.ending_pos = None
        self.direction = None
        self.label = None
        
        self.state = State.AVAILABLE
        self.crossover_type = None
        self.connecting_track_circuits = []

        for key, value in kwargs.items():
            self.__setattr__(key, value)






        # ----------------------------- Public Available Functions ----------------------------- # 


    def book(self, color):
        self.state = State.BOOKED
        self.__set_color(color)


    def set_to_main_line(self):
        # TODO :- add feature to blink for 2 seconds before changing (use Entity.blink())
        pass

    
    def set_to_change_lines(self):
        # TODO :- add feature to blink for 2 seconds before changing (use Entity.blink())
        pass






        # ----------------------------- Private Computation Functions ----------------------------- # 


    def __set_color(self, color):
        self.color = color


    def finalize(self):
        # order is important
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


        # MAJOR TODO :- remove this whole gradient color stuff and keep a simple colour
        # also delete _get_connecting_track_circuits function and connecting_track_circuit attribute
        # setting color of crossover
        match constants.CROSSOVER_ACTIVE_COLOR:
            case None:
                track_circuit_1, track_circuit_2 = self._get_connecting_track_circuits()
                self.color_1, self.color_2 = track_circuit_1.color, track_circuit_2.color
            case _:
                self.color_1, self.color_2 = constants.CROSSOVER_ACTIVE_COLOR, constants.CROSSOVER_ACTIVE_COLOR



    def _get_connecting_track_circuits(self):
        track_circuit_1_id, track_circuit_2_id = self.connecting_track_circuits

        track_circuit_1 = Database.get_component(track_circuit_1_id)
        track_circuit_2 = Database.get_component(track_circuit_2_id)

        return track_circuit_1, track_circuit_2


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


    def hide_label(self):
        if self.label:
            self.label.visible = False


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