from SwaRail.constants import State
from SwaRail import settings, Database, Type
from SwaRail.Utilities import Vec2

from ursina import Entity, Mesh, Text

class Node:
    def __init__(self, **kwargs):
        self.id = None
        self.direction = None
        self.type = None
        self.position = None

        self.station_id = ''
        self.length = 0
        self.usage = 0
        
        self.background = None
        self.label = None
        self.seperator = None


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



    def get_signals(self, direction: str) -> list:
        return self.__signals.get(direction, [])

    def add_signal(self, signal_id: str, direction: str) -> None:
        self.__signals[direction].append(signal_id)


    # ----------------------------------- UI Drawing Functions ----------------------------------- # 


    def finalize_attributes(self):
        ending_node_id = list(filter(lambda node_id: node_id.split('-')[1] == self.id.split('-')[1], self.__neighbours['>']))[0]        
        
        self.__ending_position = Database.get_node(ending_node_id).position
        self.length = Vec2.euclidian_distance(self.position, self.__ending_position)
        self.__signals['<'].reverse()

        if self.station_id != '':
            self.station_id = self.station_id.upper()
            Database.add_hault(self.station_id, self.id)


    def draw(self):
        self.draw_model()

        if self.type == Type.TRACK:
            self.draw_seperator()
            self.draw_label()
            self.draw_background()

    def draw_model(self) -> None:
        for ending_node_id in self.__neighbours['>']:
            ending_node: Node = Database.get_node(ending_node_id)
            ending_position = ending_node.position

            model = Entity(
                model=Mesh(
                    vertices=[self.position, ending_position],
                    mode='line',
                    thickness=settings.TRACK_CIRCUIT_THICKNESS,
                ),
                color=settings.TRACK_CIRCUIT_COLOR[self.direction]
            )

            Database.set_model(self.id, ending_node_id, model)

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



    # ------------------------------- Sensitive Backend Functions ------------------------------- #


    @property
    def state(self):
        return self.__state


    @state.getter
    def state(self):
        return self.state


    @state.setter
    def state(self, new_state: State):
        pass


    def __activate(self):
        pass

    def __dectivate(self):
        pass
    