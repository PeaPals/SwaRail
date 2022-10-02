from ursina import Text
from datetime import datetime
from SwaRail.Frontend import constants

class Timer:
    object = Text(
        scale=constants.TIMER_SCALE,
        color=constants.TIMER_COLOR,
        position=constants.TIMER_POSITION
    )

    @classmethod
    def update_time(cls, time = None):
        if time == None:
            time = datetime.now()

        cls.object.text = str(time)