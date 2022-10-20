from SwaRail import State, settings
from ursina import Entity, color, Vec3


class Signal:
    def __init__(self, **kwargs):
        self.id = None
        self.type = None
        self.direction = None
        self.position = None
        self.__state = State.RED
        
        self.model = None

        for key, value in kwargs.items():
            setattr(self, key, value)


    def finalize_attributes(self):
        ''' even if this is empty, its important '''
        pass

    def draw(self):
        position_offset = settings.SIGNAL_OFFSET_FROM_TRACKS

        if self.direction == '<':
            position_offset *= -1

        self.model = Entity(
            model='circle',
            color=color.red,
            scale=settings.SIGNAL_SIZE,
            position=self.position + Vec3(0, position_offset, 0) 
        )


    @property
    def state(self):
        return self.__state

    @state.getter
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

        match value:
            case State.RED: self.model.color = color.red
            case State.YELLOW: self.model.color = color.yellow
            case State.GREEN: self.model.color = color.green

