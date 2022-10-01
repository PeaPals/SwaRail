from ursina import color, Vec3, Text
import logging

# TODO :- set all colours using rgba values if colors not present in default colors of ursina

# ------------------------------------- Shared Basic Constants ------------------------------------- #


_logging_format = "%(asctime)s - %(name)s - %(levelname)s -> %(message)s [%(funcName)s:%(lineno)d]"
_log_filename = "../application.log"
logging.basicConfig(format=_logging_format, level=logging.NOTSET)


# print(color.color_names)

train_colors = [
    color.dark_gray,
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
    "=" : color.white,
    ">" : color.white,
    "<" : color.white
}

# track seperator constants
SEPERATOR_SCALE = Vec3(0.1, 0.35, 1)
SEPERATOR_COLOR = color.gray         # TODO :- is track circuit visual seperator even required?
SHOW_TRACK_CIRCUIT_SEPERATOR = True   # TODO :- remove this maybe? just control visibility using color?


# signal constants
SIGNAL_OFFSET_FROM_TRACKS = 0.25
SIGNAL_SIZE = 0.15

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
HAULT_COLOR = color.gray

# crossover constants
CROSSOVER_ACTIVE_COLOR = color.white
CROSSOVER_INACTIVE_COLOR = color.gray



# --------------------------------- MapHandler:PostParser Constants --------------------------------- #

# altering global text fields
Text.font = 'VeraMono.ttf'

# declaring constants for text labels
FIELD_TO_LABEL = ['track_circuits'] # TODO :- add label for crossover

TRACK_CIRCUIT_LABEL_COLOR = color.yellow
TRACK_CIRCUIT_LABEL_SIZE = 7
TRACK_CIRCUIT_LABEL_OFFSET = Vec3(-0.1, 0.35, 0.2)

CROSSOVER_LABEL_COLOR = color.yellow
CROSSOVER_LABEL_SIZE = 4
CROSSOVER_BASE_OFFSET = Vec3(-0.5, -0.1, 0.2)
CROSSOVER_BASE_ROTATION = Vec3(0, 0, 75)