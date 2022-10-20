from SwaRail.Utilities import Vec2
from SwaRail import settings, Type, State, Database
from SwaRail.Server import Server
import logging

from ursina import Entity, Mesh, Text, color

class Node:
    def __init__(self, **kwargs):
        self.id = None
        self.direction = None
        self.type = None
        self.position = None

        self.station_id = ''
        self.length = 0
        self.usage = 0
        
        self.model = None
        self.background = None
        self.label = None
        self.seperator = None

        self.__upcoming_train = None


        self.__state = State.AVAILABLE
        self.__neighbours = {'<': [], '>': []}
        self.__signals = {'<': [], '>': []}

        for key, value in kwargs.items():
            setattr(self, key, value)


    # ---------------------------------- General Public Functions ---------------------------------- # 


    def get_neighbours(self, direction: str) -> list:
        return self.__neighbours.get(direction, [])

    def add_neighbour(self, neighbour_id: str, direction: str) -> None:
        self.__neighbours[direction].append(neighbour_id)



    def get_all_signals(self, direction: str) -> list:
        return self.__signals.get(direction, [])

    def add_signal(self, signal_id: str, direction: str) -> None:
        self.__signals[direction].append(signal_id)


    # ----------------------------------- UI Drawing Functions ----------------------------------- # 


    def finalize_attributes(self):
        ending_node_id = list(filter(lambda node_id: node_id.split('-')[1] == self.id.split('-')[1], self.__neighbours['>']))[0]        
        
        self.__ending_position = Database.get_reference(ending_node_id).position
        self.length = Vec2.euclidian_distance(self.position, self.__ending_position)
        self.__signals['<'].reverse()


    def draw(self):
        self.draw_model()

        if self.type == Type.TRACK:
            self.draw_seperator()
            self.draw_label()
            self.draw_background()
            self.generate_tooltip()


    def draw_model(self) -> None:
        for ending_node_id in self.__neighbours['>']:
            ending_node: Node = Database.get_reference(ending_node_id)
            ending_position = ending_node.position

            self.model = Entity(
                model=Mesh(
                    vertices=[self.position, ending_position],
                    mode='line',
                    thickness=settings.TRACK_CIRCUIT_THICKNESS,
                ),
                color=settings.TRACK_CIRCUIT_COLOR[self.direction]
            )

    def draw_seperator(self):
        self.seperator = Entity(
            model='quad',
            color=settings.SEPERATOR_COLOR,
            scale=settings.SEPERATOR_SCALE,
            position=self.position
        )

        self.seperator.position.z += 1

    def draw_label(self) -> None:
        
        self.label = Text(
            text=self.id + f" ({self.station_id})" if self.station_id else self.id,
            parent=Entity(),
            color=settings.TRACK_CIRCUIT_LABEL_COLOR,
            position=((self.position + self.__ending_position)/2) + settings.TRACK_CIRCUIT_LABEL_OFFSET,
            scale=settings.TRACK_CIRCUIT_LABEL_SIZE
        )

    def draw_background(self) -> None:
        if self.station_id == '':
            return None

        self.background = Entity(
            model='quad',
            color=self.__get_background_color(),
            position=((self.position + self.__ending_position)/2) + settings.HAULT_OFFSET,
            scale=(self.length, settings.HAULT_WIDTH_FROM_TRACKS, 1)
        )

    def __get_background_color(self):
        for ending_code in settings.HAULT_COLOR.keys():
            if self.station_id.endswith(ending_code):
                return settings.HAULT_COLOR[ending_code]

        return settings.DEFAULT_HAULT_COLOR


    def generate_tooltip(self) -> None:
        pass

    def __show_tooltip(self, train_number) -> None:
        pass

    def __hide_tooltip(self) -> None:
        pass


    # ------------------------------- Sensitive Backend Functions ------------------------------- #


    @property
    def state(self):
        return self.__state


    @state.getter
    def state(self):
        return self.__state


    @state.setter
    def state(self, new_state: State):
        self.__state = new_state

        match new_state:
            case State.OCCUPIED: self.__activate()
            case State.AVAILABLE: self.__dectivate()


    @property
    def upcoming_train(self):
        return self.__upcoming_train


    @upcoming_train.setter
    def upcoming_train(self, value: str):
        self.__upcoming_train = value

    
    @upcoming_train.getter
    def upcoming_train(self):
        return self.__upcoming_train
    



    def __activate(self):
        if self.__upcoming_train == None:
            upcoming_train = Server.get_train(self.id)
            if upcoming_train == None:
                logging.critical(f"The train at {self.id} is not registered... switch to manual immediately")
                return None
            
            self.__upcoming_train = upcoming_train
        


        self.__show_tooltip(self.__upcoming_train)
        self.model.color = color.red
        self.usage += 1

        train = Database.get_train(self.__upcoming_train)
        train.currently_at = self.id

        self.notify_next_node(train)
        self.__upcoming_train = None


    def notify_next_node(self, train):
        if train.path == None or len(train.path) == 0:
            return None

        next_node_id = train.path[0]
        next_node: Node = Database.get_reference(next_node_id)
        next_node.notification(train)
        


    def notification(self, train):
        self.__upcoming_train = train.number

        for signal_id in self.__signals[train.direction]:
            signal = Database.get_reference(signal_id)
            signal.state = train.signal_seq.get()


    def __dectivate(self):
        self.__hide_tooltip()
        self.model.color = settings.TRACK_CIRCUIT_COLOR[self.direction]

        for direction in ('<', '>'):
            for signal_id in self.__signals[direction]:
                signal = Database.get_reference(signal_id)
                signal.state = State.RED


    def book(self, train_number: str, color):
        self.state = State.BOOKED
        self.model.color = color
        # self.__upcoming_train = train_number # TODO :- ?