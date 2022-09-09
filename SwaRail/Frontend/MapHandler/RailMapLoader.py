from SwaRail import constants
from SwaRail.Frontend.Components.tracks import TrackCircuit
from SwaRail.Frontend.Components.signals import Signal
from SwaRail.Frontend.Components.stations import Station
from SwaRail.Frontend.Components.crossover import Crossover
from SwaRail.Frontend.Components.seperator import Seperator
from ursina import Vec3


# MAJOR TODO :- add text labels to all track circuits ID... on them... maybe show them if zoomed in enough?


class MapParser:
    map_data = None

    TRACK_CIRCUIT_ID_COUNTER = 1
    PREV_CONNECTION = None
    CURR_TRACK_CIRCUIT = None


    @classmethod
    def parse(cls, map_name):
        
        # reading file data
        with open(constants.MAP_PATH(map_name), 'r') as map_file:
            cls.map_data = map_file.read().split('\n') # TODO :- convert path to absolute path

        # iterating through each line and parsing it
        for line_no, line in enumerate(cls.map_data):
            cls._parse_line(line, line_no)

        # logging a summary of database
        constants.logging.debug(constants.Database.summary())



    @classmethod
    def _parse_line(cls, line, Y_coordinate):

        # TODO :- make a new and clean parse_line function...
        # there is no need for a seperate details class ... just make object of class Track
        # and work on it

        for index, character in enumerate(line):
            # no need to handle space... it helps in addings offset between components on map

            # TODO :- try to calculate X_coordinate and Y_coordinate outside all functions
            # before hand for easy debugging and reducing redundancy
            if character == ' ':
                pass

            elif character in '-<>=':
                cls._update_curr_track_circuit(character, index, Y_coordinate)

            elif character in '+':
                cls._seperate_track_circuits(index, Y_coordinate)

            elif character in '\/':
                cls._add_new_crossover(character, index, Y_coordinate)

            elif character in '0123456789':
                cls._add_new_signal(character, index, Y_coordinate)

            else:
                # else is a station with station code and its mapping in railmap file
                cls._add_new_station(character, index, Y_coordinate)


        # add any remaining component to the database
        if cls.CURR_TRACK_CIRCUIT != None:
            cls._end_curr_track_circuit()

        # if cls.CURR_CROSSOVER != None:
        #     cls._end_curr_crossover(is_right_starter=True)

        # resetting used variables
        cls.TRACK_CIRCUIT_ID_COUNTER = 1
        cls.PREV_CONNECTION = None

        # finalizing all crossovers
        for crossover in constants.Database.CROSSOVERS.values():
            crossover.finalize_crossover()
            print(crossover)
            print(crossover._is_active)


    # ---------------------------- classmethods to update track circuits ---------------------------- #


    @classmethod
    def _update_curr_track_circuit(cls, character, X_coordinate, Y_coordinate):
        if cls.CURR_TRACK_CIRCUIT == None:
            cls.CURR_TRACK_CIRCUIT = TrackCircuit()
            cls.CURR_TRACK_CIRCUIT.ID = f'TC-{Y_coordinate}-{cls.TRACK_CIRCUIT_ID_COUNTER}'
            cls.CURR_TRACK_CIRCUIT.direction = constants.CHARACTER_TO_DIRECTION[character]
            cls.CURR_TRACK_CIRCUIT.connections["left"] = [] if cls.PREV_CONNECTION == None else [cls.PREV_CONNECTION.ID]
            cls.CURR_TRACK_CIRCUIT.starting_pos = Vec3(X_coordinate * constants.CHARACTER_TO_LENGTH, -constants.MAP_LINES_OFFSET * Y_coordinate, 0)
            cls.CURR_TRACK_CIRCUIT.ending_pos = Vec3(X_coordinate * constants.CHARACTER_TO_LENGTH, -constants.MAP_LINES_OFFSET * Y_coordinate, 0)

            cls.TRACK_CIRCUIT_ID_COUNTER += 1

        
        # TODO :- there is no need for this... since we can just use starting and final index 
        # to find starting and final position of the circuit track... but it isn't working
        # fid out why
        cls.CURR_TRACK_CIRCUIT.ending_pos.x += constants.CHARACTER_TO_LENGTH


    @classmethod
    def _draw_seperator_on_screen(cls):
        position = cls.CURR_TRACK_CIRCUIT.ending_pos
        Seperator(position = position)



    @classmethod
    def _seperate_track_circuits(cls, X_coordinate, Y_coordinate):
        if cls.CURR_TRACK_CIRCUIT == None: # no track circuit to seperate
            constants.logging.warn(f"Ignoring track circuit seperation request at line:{Y_coordinate+1} col:{X_coordinate+1} since its declared before track circuit and direction registration")
            return None

        cls.CURR_TRACK_CIRCUIT.ending_pos = Vec3(X_coordinate * constants.CHARACTER_TO_LENGTH, -constants.MAP_LINES_OFFSET * Y_coordinate, 0)
        cls.CURR_TRACK_CIRCUIT.ending_pos.x += constants.CHARACTER_TO_LENGTH

        # draw seperator on screen if settings allow it
        if constants.SHOW_TRACK_CIRCUIT_SEPERATOR == True:
            cls._draw_seperator_on_screen()

        cls._end_curr_track_circuit()


    @classmethod
    def _end_curr_track_circuit(cls):

        # adding this track circuit to main shared database of track circuits
        constants.Database.TRACK_CIRCUITS[cls.CURR_TRACK_CIRCUIT.ID] = cls.CURR_TRACK_CIRCUIT
        
        # finalize current object
        cls.CURR_TRACK_CIRCUIT.finalize()

        # updating class attributes
        cls.PREV_CONNECTION = cls.CURR_TRACK_CIRCUIT
        cls.CURR_TRACK_CIRCUIT = None



    # -------------------------------- classmethods to update signals -------------------------------- #


    @classmethod
    def _create_new_signal(cls, character, X_coordinate, Y_coordinate):
        
        # defining signal metadata
        signal_id = f"S-{Y_coordinate}-{X_coordinate}"
        signal_details = constants.NUMBER_TO_SIGNAL[character]
        signal_direction, signal_type = signal_details.split('-')

        if signal_direction == 'right':
            signal_position = Vec3(X_coordinate * constants.CHARACTER_TO_LENGTH, (-constants.MAP_LINES_OFFSET * Y_coordinate)  + constants.SIGNAL_OFFSET_FROM_TRACKS, 0)
        else:
            signal_position = Vec3(X_coordinate * constants.CHARACTER_TO_LENGTH, (-constants.MAP_LINES_OFFSET * Y_coordinate) - constants.SIGNAL_OFFSET_FROM_TRACKS, 0)
        
        
        # Making a new signal
        curr_signal = Signal()

        curr_signal.ID = signal_id
        curr_signal.parent_track_circuit_id = cls.CURR_TRACK_CIRCUIT.ID
        curr_signal.direction = signal_direction
        curr_signal.signal_type = signal_type
        curr_signal.position = signal_position


        return curr_signal


    @classmethod
    def _update_signal_infos(cls, signal_id, signal_direction, curr_signal):
        # updating info in main database
        constants.Database.SIGNALS[signal_id] = curr_signal

        # updating info in current track circuit
        cls.CURR_TRACK_CIRCUIT.signals[signal_direction].append(signal_id)


    @classmethod
    def _add_new_signal(cls, character, X_coordinate, Y_coordinate):

        if cls.CURR_TRACK_CIRCUIT == None:
            constants.logging.warn(f"Rejecting Signal at line:{Y_coordinate+1} col:{X_coordinate+1} since its declared before track circuit and direction registration")
            return None

        # TODO See if this is even required or not... if the above TODO of _update_curr_track_circuit()
        # is resolved... then remove this too
        cls.CURR_TRACK_CIRCUIT.ending_pos.x += constants.CHARACTER_TO_LENGTH

        # making a new signal
        curr_signal = cls._create_new_signal(character, X_coordinate, Y_coordinate)

        # update info of this signal everywhere
        cls._update_signal_infos(curr_signal.ID, curr_signal.direction, curr_signal)


    # ------------------------------ classmethods to update crossovers ------------------------------ #


    @classmethod
    def _get_crossover_ending_pos(cls, character, X_coordinate, Y_coordinate):

        for line_no in range(Y_coordinate-1, -1, -1):
            if character == '/':
                X_coordinate += 1
            else:
                X_coordinate -= 1

            if not (0 <= X_coordinate <= len(cls.map_data[line_no])):
                constants.logging.warn(f"Found no ending of crossover {character} at line:{Y_coordinate+1} col:{X_coordinate+1}, thus rejecting it")
                break

            if cls.map_data[line_no][X_coordinate] == character:
                try:
                    if (cls.map_data[line_no][X_coordinate-1] != ' ') and (cls.map_data[line_no][X_coordinate+1] != ' '):
                        ending_pos = Vec3(X_coordinate, line_no, 0)
                        return ending_pos
                except Exception as e:
                    constants.logging.warn(f"Rejecting crossover {character} ending at line:{line_no+1} col:{X_coordinate+1}. Please make sure that both side of the crossover (slash) on the railmap file is convered with any of -<>=+")
                    break
            else:
                constants.logging.warn(f"Found no ending of crossover {character} at line:{Y_coordinate+1} col:{X_coordinate+1}, thus rejecting it")
                break

        return None

    @classmethod
    def _get_crossover_ending_track_circuit(cls, ending_pos):
        counter = 1
        Y_coordinate = int(ending_pos.y)
        for index in range(int(ending_pos.x), -1, -1):
            if cls.map_data[Y_coordinate][index] == '+':
                counter += 1

        return f"TC-{Y_coordinate}-{counter}"


    @classmethod
    def _create_new_crossover(cls, character, X_coordinate, Y_coordinate):
        ending_pos = cls._get_crossover_ending_pos(character, X_coordinate, Y_coordinate)
        
        if ending_pos == None:
            return None

        ending_track_circuit_id = cls._get_crossover_ending_track_circuit(ending_pos)

        if ending_track_circuit_id == None:
            constants.logging.warn(f"Rejecting new crossover request at line:{Y_coordinate+1} col:{X_coordinate+1} since could not find its ending track circuit for ending position = {ending_pos}")
            return None
        
        curr_crossover = Crossover()
        curr_crossover.ID = f"CO-{X_coordinate}-{cls.CURR_TRACK_CIRCUIT.ID}-{ending_track_circuit_id}"
        curr_crossover.direction = "forward" if character == '/' else "backward"
        curr_crossover.starting_pos = Vec3(X_coordinate * constants.CHARACTER_TO_LENGTH, -constants.MAP_LINES_OFFSET * Y_coordinate, 0)

        ending_pos.x *= constants.CHARACTER_TO_LENGTH
        ending_pos.y *= -constants.MAP_LINES_OFFSET

        curr_crossover.ending_pos = ending_pos

        if curr_crossover.direction == 'forward':
            curr_crossover.connections['right'].append(ending_track_circuit_id)
            curr_crossover.connections['left'].append(cls.CURR_TRACK_CIRCUIT.ID)
        else:
            curr_crossover.connections['left'].append(cls.CURR_TRACK_CIRCUIT.ID)
            curr_crossover.connections['right'].append(ending_track_circuit_id)


        curr_crossover.connecting_track_circuits = [cls.CURR_TRACK_CIRCUIT.ID, ending_track_circuit_id]

        return curr_crossover


    @classmethod
    def _update_crossover_infos(cls, curr_crossover):
        # updating crossover object in database
        constants.Database.CROSSOVERS[curr_crossover.ID] = curr_crossover



    @classmethod
    def _add_new_crossover(cls, character, X_coordinate, Y_coordinate):

        # all track crossovers below line 0 will parse 0 as well... bottom-to-top
        if Y_coordinate == 0:
            return None

        if cls.CURR_TRACK_CIRCUIT == None:
            constants.logging.warn(f"Rejecting new crossover request at line:{Y_coordinate+1} col:{X_coordinate+1} since its declared before track circuit and direction registration")
            return None

        # TODO See if this is even required or not... if the above TODO of _update_curr_track_circuit()
        # is resolved... then remove this too
        cls.CURR_TRACK_CIRCUIT.ending_pos.x += constants.CHARACTER_TO_LENGTH

        # creating new crossover
        curr_crossover = cls._create_new_crossover(character, X_coordinate, Y_coordinate)

        if curr_crossover == None:
            return None

        # updating crossover infos across everywhere
        cls._update_crossover_infos(curr_crossover)








    # ------------------------------- classmethods to update stations ------------------------------- #

    @classmethod
    def _create_new_station(cls, character):
        curr_station = Station()
        curr_station.ID = f"H-{character}-{cls.CURR_TRACK_CIRCUIT.ID}"
        curr_station.main_station_id = character
        curr_station.parent_track_circuit_id = cls.CURR_TRACK_CIRCUIT.ID

        return curr_station


    @classmethod
    def _update_station_infos(cls, curr_station):
        # adding current hault to database
        constants.Database.HAULTS[curr_station.ID] = curr_station

        # adding current hault to a station
        if constants.Database.STATIONS.get(curr_station.main_station_id, False):
            constants.Database.STATIONS[curr_station.main_station_id].append(curr_station.ID)
        else:
            constants.Database.STATIONS[curr_station.main_station_id] = [curr_station.ID]


    @classmethod
    def _add_new_station(cls, character, X_coordinate, Y_coordinate):
        
        if cls.CURR_TRACK_CIRCUIT == None:
            constants.logging.warn(f"Rejecting hault (station) request at line:{Y_coordinate+1} col:{X_coordinate+1} since its declared before track circuit and direction registration")
            return None

        
        # TODO See if this is even required or not... if the above TODO of _update_curr_track_circuit()
        # is resolved... then remove this too
        cls.CURR_TRACK_CIRCUIT.ending_pos.x += constants.CHARACTER_TO_LENGTH


        if cls.CURR_TRACK_CIRCUIT.hault_id != None:
            constants.logging.warn(f"Ignoring hault (station) request at line:{Y_coordinate+1} col:{X_coordinate+1} since the track circuit is already a haulting track")
            return None

        #creating new station
        curr_station = cls._create_new_station(character)

        # registering track circuit as a haulting section
        cls.CURR_TRACK_CIRCUIT.hault_id = curr_station.ID

        # update station infos
        cls._update_station_infos(curr_station)