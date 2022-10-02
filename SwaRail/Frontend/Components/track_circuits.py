from ursina import Entity, Mesh, Text
from SwaRail.Frontend import constants
from SwaRail.Frontend.Components.stations import Hault
from SwaRail.database import Database, State

class TrackCircuit(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.ID = None
        self.starting_pos = None
        self.ending_pos = None
        self.direction = None
        self.color = None
        self.length = 0
        self.label = None
        self.station_ID = ''
        self.hault_object = None

        for key, value in kwargs.items():
            self.__setattr__(key, value)


    def finalize(self):
        # order is important

        self.finalize_attributes()
        self.finalize_hault()
        self.draw()


    def finalize_attributes(self):
        # setting color
        self.color = constants.TRACK_CIRCUIT_COLOR[self.direction]
        
        # setting length of track circuit in KMs
        line_length = self.ending_pos.x - self.starting_pos.x
        self.length = round(line_length * 100) / 1000


    def finalize_hault(self):
        match self.station_ID:
            case '': return None
        
        self.station_ID = self.station_ID.upper()
        self.hault_object = Hault(self.starting_pos, self.ending_pos)
        Database.add_hault(self.station_ID, self.ID)

        self.hault_object.finalize()


    def draw(self):
        # setting model of track_circuit
        self.model = Mesh(
            vertices=[self.starting_pos, self.ending_pos],
            colors=[self.color, self.color],
            mode='line', 
            thickness=constants.TRACK_CIRCUIT_THICKNESS
        )



    def _get_label_position(self):
        position = (self.starting_pos + self.ending_pos) / 2        
        position += constants.TRACK_CIRCUIT_LABEL_OFFSET

        return position


    def _create_label(self):
        label_text = self.ID

        match self.station_ID:
            case '': pass
            case _: label_text += f" ({self.station_ID})"
        
        
        self.label = Text(
            text = label_text,
            parent = Entity(),
            color = constants.TRACK_CIRCUIT_LABEL_COLOR,
            position = self._get_label_position(),
            scale = constants.TRACK_CIRCUIT_LABEL_SIZE
        )


    def show_label(self):
        if self.label == None:
            self._create_label()

        self.label.visible = True


    def book(self, color):
        Database.state[self.ID] = State.BOOKED
        self.set_color(color)


    def set_color(self, color):
        self.color = color


    def __str__(self):
        return f'''
        I Am A Track Circuit
        ID = {self.ID}, starting pos = {self.starting_pos}, ending pos = {self.ending_pos}, length = {self.length} KM,
        direction is {self.direction}, color = {self.color}
        '''

    def input(self, key):
        pass

    def update(self):
        pass