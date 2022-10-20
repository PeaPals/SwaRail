from ursina import Text
from datetime import datetime
from SwaRail import settings

class Timer:
    object = Text(
        scale=settings.TIMER_SCALE,
        color=settings.TIMER_COLOR,
        position=settings.TIMER_POSITION
    )
    

    @classmethod
    def update_time(cls, time = None):
        if time == None:
            time = datetime.now()

        cls.object.text = time.strftime(f"%d %b %y  %H:%M:%S")