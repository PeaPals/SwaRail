from ursina import color
import logging
from SwaRail.Utilities.database_handler import Database


# TODO :- set all colours using rgba values if colors not present in default colors of ursina

# ------------------------------------- Shared Basic Constants ------------------------------------- #


_logging_format = "%(asctime)s - %(name)s - %(levelname)s -> %(message)s [%(funcName)s:%(lineno)d]"
_log_filename = "../application.log"
logging.basicConfig(format=_logging_format, level=logging.NOTSET)


# print(color.color_names)
colors = [
    color.white,
    color.smoke,
    color.light_gray,
    color.gray,
    color.dark_gray,
    color.black,
    color.red,
    color.orange,
    color.yellow,
    color.lime,
    color.green,
    color.turquoise,
    color.cyan,
    color.azure,
    color.blue,
    color.violet,
    color.magenta,
    color.pink,
    color.brown,
    color.olive,
    color.peach,
    color.gold,
    color.salmon
]




# ------------------------------------- Config Constants ------------------------------------- #


CAMERA_NAVIGATION_SPEED = 6


# ------------------------------------- MapHandler Constants ------------------------------------- #

# parser constants
MAP_PATH = lambda map_name : f"Data/Maps/{map_name}.railmap"
MAP_LINES_OFFSET = 1

# track circuit constants
TRACK_CIRCUIT_THICKNESS = 4.5
CHARACTER_TO_LENGTH = 0.3     # 0.3 = 30 m

TRACK_CIRCUIT_COLOR = {
    "=" : color.yellow,
    ">" : color.pink,
    "<" : color.azure
}

# track seperator constants
SEPERATOR_SCALE = (0.1, 0.35, 1)
SEPERATOR_COLOR = color.green         # TODO :- is track circuit visual seperator even required?
SHOW_TRACK_CIRCUIT_SEPERATOR = True   # TODO :- remove this maybe? just control visibility using color?


# signal constants
SIGNAL_OFFSET_FROM_TRACKS = 0.25
SIGNAL_SIZE = 0.12

NUMBER_TO_SIGNAL = {
    '0' : '>-YRYG',
    '9' : '<-YRYG',
    
    '1' : '>-YRYG',
    '2' : '>-RYG',
    '3' : '>-YR',
    '4' : '>-GR',

    '5' : '<-YRYG',
    '6' : '<-RYG',
    '7' : '<-YR',
    '8' : '<-GR'
}

# station constants
HAULT_WIDTH_FROM_TRACKS = 0.35
HAULT_COLOR = color.dark_gray

# crossover constants
CROSSOVER_ACTIVE_COLOR = None
CROSSOVER_INACTIVE_COLOR = color.gray