from SwaRail import constants
from SwaRail.Frontend.Components import Crossover, Seperator, Signal, Hault, TrackCircuit
from ursina import Vec3
from SwaRail.Frontend.MapHandler.postparser import PostParser
from SwaRail.database import Database
from SwaRail.Utilities.mathematical import Vec2
import logging


# MAJOR TODO :- Make Command Panel

# Major TODO :- insert a special token @ to show connection between two different sections.
# It will represent the area connected by Automatic Block Signalling.


class MapParser:
    MAP_DATA = None
    CURR_TRACK_CIRCUIT = None
    COORDINATES = Vec2(0, 0)



    @classmethod
    def parse(cls, map_name):
        cls._parse(map_name)
        PostParser.start_postparsing_operations()


    @classmethod
    def _parse(cls, map_name):
        
        # reading file data
        with open(constants.MAP_PATH(map_name), 'r') as map_file:
            cls.MAP_DATA = map_file.read().split('\n') # TODO :- convert path to absolute path

        # saving map data to database for future use
        Database.railmap = cls.MAP_DATA

        # iterating through each line and parsing it
        for line_no, line in enumerate(cls.MAP_DATA):
            cls.COORDINATES.Y = line_no
            cls._parse_line(line)


    @classmethod
    def _parse_line(cls, line):


        for index, character in enumerate(line):

            # setting X_coordinate
            cls.COORDINATES.X = index
            
            # starting check
            match character:
                case ' ': cls._end_curr_track_circuit()
                case '-' : continue
                case '<'|'>'|'=' : cls._start_new_track_circuit(character)
                case '/'|'\\' : cls._start_new_crossover(character)
                case '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9' : cls._add_new_signal(character)
                case _ : cls._set_new_hault(character)  # else is a station with station code and its mapping in railmap file


        # add any remaining component to the database
        if cls.CURR_TRACK_CIRCUIT != None:
            cls.COORDINATES.X += 1
            cls._end_curr_track_circuit()


    # ------------------------- classmethods for general use by all methods ------------------------- #
    

    @classmethod
    def _get_id(cls, id_prefix, *args):
        id = f"{id_prefix}-{cls.COORDINATES.Y}-{cls.COORDINATES.X}"

        for arg in args:
            id += f'-{arg}'

        return id


    @classmethod
    def _add_to_database(cls, component):
        Database.add_component(component)


    @classmethod
    def _get_position(cls, X=None, Y=None):
        # will give current position if X and Y are absent

        match X:
            case None: X = cls.COORDINATES.X

        match Y:
            case None: Y = cls.COORDINATES.Y
        
        return Vec3(X * constants.CHARACTER_TO_LENGTH, -constants.MAP_LINES_OFFSET * Y, 0)

        # Major TODO : change above vector to COORDINATE * offset = map coordinates and save only COORDINATE inside object


    # ---------------------------- classmethods to update track circuits ---------------------------- #

    @classmethod
    def _create_new_track_circuit(cls, character):
        # making new track circuit
        new_track_circuit = TrackCircuit(
            ID = cls._get_id('TC'),
            direction = character,
            starting_pos = cls._get_position(),
        )

        # registering this track circuit as a node in main graph
        Database.register_graph_node(new_track_circuit)

        return new_track_circuit


    @classmethod
    def _start_new_track_circuit(cls, character):
        new_track_circuit = cls._create_new_track_circuit(character)

        # connecting new and old (curr) track circuit
        cls._connect_track_circuits(cls.CURR_TRACK_CIRCUIT, new_track_circuit)

        # ending old (curr) track circuit
        cls._end_curr_track_circuit()

        # making new circuit as curr circuit
        cls.CURR_TRACK_CIRCUIT = new_track_circuit


    @classmethod
    def _create_visible_track_seperator(cls):
        if constants.SHOW_TRACK_CIRCUIT_SEPERATOR:
            seperator = Seperator(ID = cls._get_id('SP'), position=cls._get_position())

            # adding to database
            cls._add_to_database(seperator)


    @classmethod
    def _connect_track_circuits(cls, left_tc, right_tc):
        if left_tc == None or right_tc == None:
            return None

        # adding a visual seperator (useful if everything is of single colour)
        cls._create_visible_track_seperator()

        # updating connections
        Database.add_graph_connection(left_tc, right_tc)


    @classmethod
    def _end_curr_track_circuit(cls):
        if cls.CURR_TRACK_CIRCUIT == None:
            return None

        cls.CURR_TRACK_CIRCUIT.ending_pos = cls._get_position()

        # adding curr track circuit to database
        cls._add_to_database(cls.CURR_TRACK_CIRCUIT)

        # resetting current track circuit variable
        cls.CURR_TRACK_CIRCUIT = None



    # -------------------------------- classmethods to update signals -------------------------------- #


    @classmethod
    def _add_new_signal(cls, character):
        if cls.CURR_TRACK_CIRCUIT == None:
            logging.warning(f"Signal at LINE:{cls.COORDINATES.Y + 1} COL:{cls.COORDINATES.X + 1} has been ignored since it is declared before a track circuit")
            return None

        new_signal = cls._create_new_signal(character)
        cls._bind_signal_to_track_circuit(new_signal)
        cls._add_to_database(new_signal)


    @classmethod
    def _bind_signal_to_track_circuit(cls, signal):
        cls.CURR_TRACK_CIRCUIT.signals[signal.direction].append(signal.ID)


    @classmethod
    def _create_new_signal(cls, character):
        direction, signal_type = constants.NUMBER_TO_SIGNAL[character].split('-')
        position = cls._get_position()


        match direction:
            case '>' : position.y += constants.SIGNAL_OFFSET_FROM_TRACKS
            case '<' : position.y -= constants.SIGNAL_OFFSET_FROM_TRACKS


        new_signal = Signal(
            ID = cls._get_id('SI'),
            direction = direction,
            signal_type = signal_type,
            parent_track_circuit_id = cls.CURR_TRACK_CIRCUIT.ID,
            position = position
        )

        return new_signal


    # ------------------------------ classmethods to update crossovers ------------------------------ #


    @classmethod
    def _start_new_crossover(cls, character):
        if cls.CURR_TRACK_CIRCUIT == None:
            logging.debug(f"Crossover at LINE:{cls.COORDINATES.Y + 1} COL:{cls.COORDINATES.X + 1} has been ignored since it is declared before a track circuit")
            return None
        
        # get end point of this crossover
        ending_pos = cls._get_crossover_ending_pos(character)

        if ending_pos == None:
            logging.debug(f"No ending for crossover of type {character} at LINE:{cls.COORDINATES.Y + 1} COL:{cls.COORDINATES.X + 1}")
            return None

        # get ending track circuit id of this crossover
        ending_track_circuit = cls._get_ending_track_circuit_id(ending_pos)

        if ending_track_circuit == None:
            logging.debug(f"No valid track circuit was found for crossover of type {character} at LINE:{cls.COORDINATES.Y + 1} COL:{cls.COORDINATES.X + 1}, ending at :- LINE:{ending_pos.Y + 1} COL:{ending_pos.X + 1}")
            return None
        
        # making a new crossover
        new_crossover = cls._create_new_crossover(character, ending_pos)

        # update crossover infos everywhere
        cls._update_crossover_info(new_crossover, ending_track_circuit)


    @classmethod
    def _get_crossover_ending_pos(cls, crossover_type):
        X_direction_adder = 0

        match crossover_type:
            case '/': X_direction_adder = 1
            case '\\': X_direction_adder = -1

        return cls.__get_crossover_ending_pos(X_direction_adder, crossover_type)
        

    @classmethod
    def __get_crossover_ending_pos(cls, X_direction_adder, crossover_type):
        line_number = cls.COORDINATES.Y
        character_number = cls.COORDINATES.X

        while line_number > 0:
            character_number += X_direction_adder
            line_number -= 1

            if not (0 < character_number <= len(cls.MAP_DATA[line_number])-1):
                return None

            current_line = cls.MAP_DATA[line_number]

            if not current_line[character_number] == crossover_type:
                return None

            if not current_line[character_number-1] == ' ':
                return Vec2(character_number, line_number)


    @classmethod
    def _get_ending_track_circuit_id(cls, ending_pos):
        line_number = ending_pos.Y
        ending_line = cls.MAP_DATA[line_number]

        character_number = ending_pos.X

        while character_number >= 0:
            character_number -= 1

            if ending_line[character_number] in ('<', '>', '='):
                track_id = f'TC-{line_number}-{character_number}'
                return Database.get_component(track_id)

        return None


    @classmethod
    def _create_new_crossover(cls, character, ending_pos):
        new_crossover = Crossover(
            ID = cls._get_id('CO', ending_pos.Y, ending_pos.X),
            crossover_type = character,
            starting_pos = cls._get_position(),
            ending_pos = cls._get_position(ending_pos.X, ending_pos.Y),
            direction = '='
        )

        # registering this as a graph node in database
        Database.register_graph_node(new_crossover)

        return new_crossover


    @classmethod
    def _update_crossover_info(cls, new_crossover, ending_track_circuit):

        # adding crossover to database
        cls._add_to_database(new_crossover)

        # updating connecting track circuits
        new_crossover.connecting_track_circuits = [cls.CURR_TRACK_CIRCUIT.ID, ending_track_circuit.ID]

        # updating connections
        match new_crossover.crossover_type:
            case '/':
                Database.add_graph_connection(cls.CURR_TRACK_CIRCUIT, new_crossover)
                Database.add_graph_connection(new_crossover, ending_track_circuit)

            case '\\':
                Database.add_graph_connection(ending_track_circuit, new_crossover)
                Database.add_graph_connection(new_crossover, cls.CURR_TRACK_CIRCUIT)


    # ------------------------------- classmethods to update stations ------------------------------- #


    @classmethod
    def _set_new_hault(cls, character):
        if cls.CURR_TRACK_CIRCUIT == None:
            logging.warning(f"Hault/Platform at LINE:{cls.COORDINATES.Y + 1} COL:{cls.COORDINATES.X + 1} has been ignored since it is declared before a track circuit")
            return None

        # adding current character to hault name
        cls.CURR_TRACK_CIRCUIT.station_id += character