from ursina import color
import logging
from SwaRail.Utilities.DatabaseHandler import Database


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

CHARACTER_TO_DIRECTION = {
    '-' : 'bi',
    '=' : 'bi',
    '<' : 'left',
    '>' : 'right'
}


# track circuit constants
TRACK_CIRCUIT_THICKNESS = 4.5
CHARACTER_TO_LENGTH = 0.3     # 0.3 = 30 m

TRACK_CIRCUIT_COLOR = {
    "bi" : color.yellow,
    "right" : color.pink,
    "left" : color.azure
}


# track seperator constants
SHOW_TRACK_CIRCUIT_SEPERATOR = False
SEPERATOR_SCALE = (0.1, 0.35, 1)
SEPERATOR_COLOR = color.pink

# TODO :- remove this maybe?
if len(set(TRACK_CIRCUIT_COLOR.values())) == 1:
    SHOW_TRACK_CIRCUIT_SEPERATOR = True


# signal constants
SIGNAL_OFFSET_FROM_TRACKS = 0.25
SIGNAL_SIZE = 0.12

NUMBER_TO_SIGNAL = {
    '0' : 'right-YRYG',
    '9' : 'left-YRYG',
    
    '1' : 'right-YRYG',
    '2' : 'right-RYG',
    '3' : 'right-YR',
    '4' : 'right-GR',

    '5' : 'left-YRYG',
    '6' : 'left-RYG',
    '7' : 'left-YR',
    '8' : 'left-GR'
}

# station constants
HAULT_WIDTH_FROM_TRACKS = 0.35
HAULT_COLOR = color.dark_gray

# crossover constants
CROSSOVER_INACTIVE_COLOR = color.gray