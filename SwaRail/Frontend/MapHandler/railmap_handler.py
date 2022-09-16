from SwaRail import constants
from SwaRail.Frontend.Components import Crossover, Seperator, Signal, Station, TrackCircuit
from ursina import Vec3
from dataclasses import dataclass


@dataclass
class Vec2:
    X : int
    Y : int


class MapParser:
    map_data = None

    TRACK_CIRCUIT_ID_COUNTER = 1
    PREV_CONNECTION = None
    CURR_TRACK_CIRCUIT = None

    COORDINATE = Vec2(0, 0)


    @classmethod
    def parse(cls, map_name):
        
        # reading file data
        with open(constants.MAP_PATH(map_name), 'r') as map_file:
            cls.map_data = map_file.read().split('\n') # TODO :- convert path to absolute path

        # iterating through each line and parsing it
        for line_no, line in enumerate(cls.map_data):
            # setting Y_coordinate and then parsing current line
            cls.COORDINATE.Y = line_no
            cls._parse_line(line)

        # logging a summary of database
        constants.logging.debug(constants.Database.summary())



    @classmethod
    def _parse_line(cls, line):


        for index, character in enumerate(line):

            # setting X_coordinate
            cls.COORDINATE.X = index
            
            # starting checks
            if character == ' ':
                cls._seperate_track_circuits(warning=False)

            elif character in '-<>=':
                cls._update_curr_track_circuit(character)

            elif character in '+':
                cls._seperate_track_circuits()

            elif character in '\/':
                cls._add_new_crossover(character)

            elif character in '0123456789':
                cls._add_new_signal(character)

            else:
                # else is a station with station code and its mapping in railmap file
                cls._add_new_station(character)


        # add any remaining component to the database
        if cls.CURR_TRACK_CIRCUIT != None:
            # cls._end_curr_track_circuit()
            cls.COORDINATE.X = len(line)-1
            cls._seperate_track_circuits()

        # resetting used variables
        cls.TRACK_CIRCUIT_ID_COUNTER = 1
        cls.PREV_CONNECTION = None

        # finalizing all crossovers
        for crossover in constants.Database.CROSSOVERS.values():
            crossover.finalize_crossover()




    # ---------------------------- classmethods to update track circuits ---------------------------- #


    @classmethod
    def _update_curr_track_circuit(cls, character):
        if cls.CURR_TRACK_CIRCUIT == None:
            cls.CURR_TRACK_CIRCUIT = TrackCircuit()
            cls.CURR_TRACK_CIRCUIT.ID = f'TC-{cls.COORDINATE.Y}-{cls.TRACK_CIRCUIT_ID_COUNTER}'
            cls.CURR_TRACK_CIRCUIT.direction = constants.CHARACTER_TO_DIRECTION[character]
            cls.CURR_TRACK_CIRCUIT.connections["left"] = [] if cls.PREV_CONNECTION == None else [cls.PREV_CONNECTION.ID]
            cls.CURR_TRACK_CIRCUIT.starting_pos = Vec3(cls.COORDINATE.X * constants.CHARACTER_TO_LENGTH, -constants.MAP_LINES_OFFSET * cls.COORDINATE.Y, 0)

            cls.TRACK_CIRCUIT_ID_COUNTER += 1


    @classmethod
    def _draw_seperator_on_screen(cls):
        position = cls.CURR_TRACK_CIRCUIT.ending_pos
        Seperator(position = position)


    @classmethod
    def _seperate_track_circuits(cls, warning=True):
        if cls.CURR_TRACK_CIRCUIT == None: # no track circuit to seperate
            if Warning == True:
                constants.logging.warn(f"Ignoring track circuit seperation request at line:{cls.COORDINATE.Y+1} col:{cls.COORDINATE.X+1} since its declared before track circuit and direction registration")
            return None

        cls.CURR_TRACK_CIRCUIT.ending_pos = Vec3(cls.COORDINATE.X * constants.CHARACTER_TO_LENGTH, -constants.MAP_LINES_OFFSET * cls.COORDINATE.Y, 0)
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
    def _create_new_signal(cls, character):
        
        # defining signal metadata
        signal_details = constants.NUMBER_TO_SIGNAL[character]
        signal_direction, signal_type = signal_details.split('-')

        if signal_direction == 'right':
            signal_position = Vec3(cls.COORDINATE.X * constants.CHARACTER_TO_LENGTH, (-constants.MAP_LINES_OFFSET * cls.COORDINATE.Y)  + constants.SIGNAL_OFFSET_FROM_TRACKS, 0)
        else:
            signal_position = Vec3(cls.COORDINATE.X * constants.CHARACTER_TO_LENGTH, (-constants.MAP_LINES_OFFSET * cls.COORDINATE.Y) - constants.SIGNAL_OFFSET_FROM_TRACKS, 0)
        
        
        # Making a new signal
        curr_signal = Signal()

        curr_signal.ID = f"SI-{cls.COORDINATE.Y}-{cls.COORDINATE.X}"
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
    def _add_new_signal(cls, character):

        if cls.CURR_TRACK_CIRCUIT == None:
            constants.logging.warn(f"Rejecting Signal at line:{cls.COORDINATE.Y+1} col:{cls.COORDINATE.X+1} since its declared before track circuit and direction registration")
            return None

        # making a new signal
        curr_signal = cls._create_new_signal(character)

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

            if not (0 <= X_coordinate < len(cls.map_data[line_no])):
                constants.logging.warn(f"Found no ending of crossover {character} at line:{Y_coordinate+1} col:{X_coordinate+1}, thus rejecting it")
                break

            if cls.map_data[line_no][X_coordinate] == character:
                try:
                    if (cls.map_data[line_no][X_coordinate-1] != ' ') and (cls.map_data[line_no][X_coordinate+1] != ' '):
                        ending_pos = Vec3(X_coordinate, line_no, 0)
                        return ending_pos
                except IndexError as e:
                    constants.logging.warn(f"Rejecting crossover {character} ending at line:{line_no+1} col:{X_coordinate+1}. Please make sure that both side of the ending crossover (slash) on the railmap file is covered with any of -<>=+")
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
    def _create_new_crossover(cls, character):
        ending_pos = cls._get_crossover_ending_pos(character, cls.COORDINATE.X, cls.COORDINATE.Y)
        
        if ending_pos == None:
            return None

        ending_track_circuit_id = cls._get_crossover_ending_track_circuit(ending_pos)

        if ending_track_circuit_id == None:
            constants.logging.warn(f"Rejecting new crossover request at line:{cls.COORDINATE.Y+1} col:{cls.COORDINATE.X+1} since could not find its ending track circuit for ending position = {ending_pos}")
            return None
        
        curr_crossover = Crossover()
        curr_crossover.ID = f"CO-{cls.COORDINATE.Y}-{cls.COORDINATE.X}"
        curr_crossover.direction = "forward" if character == '/' else "backward"
        curr_crossover.starting_pos = Vec3(cls.COORDINATE.X * constants.CHARACTER_TO_LENGTH, -constants.MAP_LINES_OFFSET * cls.COORDINATE.Y, 0)

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

        # updating crossover info to track circuits
        starting_track_circuit = cls.CURR_TRACK_CIRCUIT
        ending_track_circuit_id = curr_crossover.connecting_track_circuits[1]
        ending_track_circuit = constants.Database.TRACK_CIRCUITS[ending_track_circuit_id]

        if curr_crossover.direction == 'forward':
            starting_track_circuit.connections['right'].append(curr_crossover.ID)
            ending_track_circuit.connections['left'].append(curr_crossover.ID)

        else:
            starting_track_circuit.connections['left'].append(curr_crossover.ID)
            ending_track_circuit.connections['right'].append(curr_crossover.ID)



    @classmethod
    def _add_new_crossover(cls, character):

        # all track crossovers below line 0 will parse 0 as well... bottom-to-top
        if cls.COORDINATE.Y == 0:
            return None

        if cls.CURR_TRACK_CIRCUIT == None:
            constants.logging.warn(f"Rejecting new crossover request at line:{cls.COORDINATE.Y+1} col:{cls.COORDINATE.X+1} since its declared before track circuit and direction registration")
            return None

        # creating new crossover
        curr_crossover = cls._create_new_crossover(character)

        if curr_crossover == None:
            return None

        # updating crossover infos across everywhere
        cls._update_crossover_infos(curr_crossover)




    # ------------------------------- classmethods to update stations ------------------------------- #

    @classmethod
    def _create_new_station(cls, character):
        curr_station = Station()
        curr_station.ID = f"ST-{character}-{cls.CURR_TRACK_CIRCUIT.ID}"
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
    def _add_new_station(cls, character):
        
        if cls.CURR_TRACK_CIRCUIT == None:
            constants.logging.warn(f"Rejecting hault (station) request at line:{cls.COORDINATE.Y+1} col:{cls.COORDINATE.X+1} since its declared before track circuit and direction registration")
            return None


        if cls.CURR_TRACK_CIRCUIT.hault_id != None:
            constants.logging.warn(f"Ignoring hault (station) request at line:{cls.COORDINATE.Y+1} col:{cls.COORDINATE.X+1} since the track circuit is already a haulting track")
            return None

        #creating new station
        curr_station = cls._create_new_station(character)

        # registering track circuit as a haulting section
        cls.CURR_TRACK_CIRCUIT.hault_id = curr_station.ID

        # update station infos
        cls._update_station_infos(curr_station)



    # ------------------------------- classmethods to update text labels ------------------------------- #

    # MAJOR TODO :- add text labels to all track circuits ID... on them... maybe show them if zoomed in enough?
    @classmethod
    def _add_text_labels(cls):
        from ursina import Text

        Text.size = 0.05
        Text.default_resolution = 1080 * Text.size
        info = Text(text="A powerful waterfall roaring on the mountains")
        info.x = -0.5
        info.y = 0.4
        info.background = True
        info.visible = False                    # Do not show this text
        
        raise NotImplementedError