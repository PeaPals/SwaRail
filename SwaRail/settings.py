from ursina import color, Vec3, Text
import logging

# TODO :- set all colours using rgba values if colors not present in default colors of ursina




# -------------------------------------------------------------------------------------------------- #
# --------------------------------------- Backend Constants ---------------------------------------- #
# -------------------------------------------------------------------------------------------------- #


# -------------------------------------- A* Search Constants --------------------------------------- #

COST = {
    'TC-TC': 1,
    'TC-CO': 4,
    'CO-TC': 4,
    'CO-CO': 2,
}


# -------------------------------------------------------------------------------------------------- #
# --------------------------------------- Frontend Constants --------------------------------------- #
# -------------------------------------------------------------------------------------------------- #


# ------------------------------------- Shared Basic Constants ------------------------------------- #


_LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s -> %(message)s [%(funcName)s:%(lineno)d]"
_LOG_FILENAME = "../SwaRail.log"
logging.basicConfig(format=_LOGGING_FORMAT, level=logging.NOTSET)#, filename=_LOG_FILENAME, filemode='w')


# ------------------------------------- Config Constants ------------------------------------- #


CAMERA_NAVIGATION_SPEED = 10
TIMER_SCALE = 3
TIMER_COLOR = color.gold
TIMER_POSITION = Vec3(-0.3, 0.45, 0)


# ------------------------------------- MapHandler Constants ------------------------------------- #

# parser constants
MAP_PATH = lambda map_name : f"Data/Maps/{map_name}.railmap"
MAP_LINES_OFFSET = 1
CHARACTER_TO_LENGTH = 0.3     # 0.3 = 30 m
MAP_MULTIPLIER = Vec3(CHARACTER_TO_LENGTH, -MAP_LINES_OFFSET, 1)

# track circuit constants
TRACK_CIRCUIT_THICKNESS = 4.5

TRACK_CIRCUIT_COLOR = {
    "=" : color.white,
    ">" : color.white,
    "<" : color.white
}

DIRECTIONMAP_TRACK_CIRCUIT_COLOR = {   # TODO :- implement this in command panel
    "=" : color.pink,
    ">" : color.gold,
    "<" : color.azure
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
HAULT_OFFSET = Vec3(0, 0, 0.1)
DEFAULT_HAULT_COLOR = color.gray
HAULT_COLOR = {
    '~' : color.gold,
    'SHED': color.azure,
    'DEAD': color.red
}

# crossover constants
CROSSOVER_ACTIVE_COLOR = color.white
CROSSOVER_INACTIVE_COLOR = color.gray



# --------------------------------- MapHandler:PostParser Constants --------------------------------- #

# altering global text fields
Text.font = 'VeraMono.ttf'

# declaring constants for text labels
FIELD_TO_LABEL = {'track_circuits'} # TODO :- add label for crossover

TRACK_CIRCUIT_LABEL_COLOR = color.gold
TRACK_CIRCUIT_LABEL_SIZE = 7
TRACK_CIRCUIT_LABEL_OFFSET = Vec3(-0.1, 0.35, 0.2)

CROSSOVER_LABEL_COLOR = color.yellow
CROSSOVER_LABEL_SIZE = 4
CROSSOVER_BASE_OFFSET = Vec3(-0.5, -0.1, 0.2)
CROSSOVER_BASE_ROTATION = Vec3(0, 0, 75)

# ------------------------------------- Command Panel Constants ------------------------------------- #

COMMAND_PANEL_TOGGLE_BUTTON = 'c'
COMMAND_PANEL_POSITION = Vec3(-0.55, -0.45, 0)
COMMAND_PANEL_COLOR = color.black
COMMAND_PANEL_CHARACTER_LIMIT = 70
