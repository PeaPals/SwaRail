from ursina import Entity, Mesh, Text
from SwaRail import constants
from SwaRail.Frontend.Components.stations import Hault
from SwaRail.database import Database, State



class TrackCircuit(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.ID = None

        self.starting_pos = None
        self.ending_pos = None
        self.model = None
        self.color = None
        self.background = None    # TODO :- for some places I have used 'background' and for others 'hault'
        
        self.label = None
        self.direction = None
        self.length = 0
        self.usage = 0
        self.state = State.AVAILABLE
        
        self.signals = {'<': [], '>': []}
        self.station_id = ''

        for key, value in kwargs.items():
            self.__setattr__(key, value)


        # ----------------------------- Public Available Functions ----------------------------- # 




    def activate(self):
        pass


    def deactivate(self):
        pass


    def book(self, color):
        self.state = State.BOOKED
        self.__set_color(color)








        # ----------------------------- Private Computation Functions ----------------------------- # 

    
    def __set_color(self, color):
        self.color = color


    def finalize(self):
        # order is important

        self.__finalize_attributes()
        self.__finalize_signals()
        self.__finalize_background()
        self.__draw()


    def __finalize_attributes(self):
        # setting color
        self.__set_color(color=constants.TRACK_CIRCUIT_COLOR[self.direction])
        
        # setting length of track circuit in KMs
        line_length = self.ending_pos.x - self.starting_pos.x
        self.length = round(line_length * 100) / 1000


    def __finalize_signals(self):
        self.signals['<'].reverse()


    def __finalize_background(self):
        if self.station_id:
            self.station_id = self.station_id.upper()
            self.background = Hault(self.station_id, self.starting_pos, self.ending_pos)
            Database.add_hault(self.station_id, self.ID)
            self.background.finalize()


    def __draw(self):
        # setting model of track_circuit
        self.model = Mesh(
            vertices=[self.starting_pos, self.ending_pos],
            colors=[self.color, self.color],
            mode='line', 
            thickness=constants.TRACK_CIRCUIT_THICKNESS
        )


    def __get_label_position(self):
        position = (self.starting_pos + self.ending_pos) / 2        
        position += constants.TRACK_CIRCUIT_LABEL_OFFSET

        return position


    def __create_label(self):
        label_text = self.ID

        if self.station_id:
            label_text = self.ID + f" ({self.station_id})"
        
        
        self.label = Text(
            text = label_text,
            parent = Entity(),
            color = constants.TRACK_CIRCUIT_LABEL_COLOR,
            position = self.__get_label_position(),
            scale = constants.TRACK_CIRCUIT_LABEL_SIZE
        )


    def show_label(self):
        if self.label == None:
            self.__create_label()

        self.label.visible = True

    
    def hide_label(self):
        if self.label:
            self.label.visible = False


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