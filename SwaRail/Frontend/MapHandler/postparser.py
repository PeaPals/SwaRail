from SwaRail.Frontend import constants
from SwaRail.database import Database

# Major TODO :- use train numbers as a tooltip.
# Bind those tooltip to the track circuit, on which the head of train is.


class PostParser():

    @classmethod
    def start_postparsing_operations(cls):
        
        # visual stuff
        cls._finalize_all_components()
        cls._add_text_labels()

        # validation stuff
        cls.validate_connections_directions()
        cls.validate_neighbours_orders()
        
        # altering graph for partial neighbour use
        cls._add_indexing_to_crossovers()

        # generating optimized database to be used by backend
        # cls._generate_tracks()
        # cls._generate_junctions()

        # final summary
        cls.summary()


    # ------------------------------- classmethods for global use ------------------------------- #


    @classmethod
    def summary(cls):
        constants.logging.debug(Database.summary())


    # ------------------------------- classmethods to update graphs ------------------------------- #


    @classmethod
    def _get_direction_validated_neighbours(cls, component_id, component_direction):
        updated_neighbours = []

        for neighbour_id in Database.get_neighbours(component_id, component_direction):
            neighbour = Database.get_component(neighbour_id)

            if neighbour.direction in (component_direction, '='):
                updated_neighbours.append(neighbour_id)
            else:
                constants.logging.debug(f"{component_id} and {neighbour_id} found to have opposite directions : {component_direction} and {neighbour.direction} respectively, thus breaking the connection between them")

        return updated_neighbours


    @classmethod
    def validate_connections_directions(cls):
        for component_id in Database.graph.keys():
            for component_direction in Database.graph[component_id].keys():
                updated_neighbours = cls._get_direction_validated_neighbours(component_id, component_direction)
                Database.graph[component_id][component_direction] = updated_neighbours


    @classmethod
    def validate_neighbours_orders(cls):
        for track_circuit_id in Database.get_all_ids('TC'):
            cls._reorder(track_circuit_id)

    @classmethod
    def _get_index(cls, neighbours, track_circuit_id, crossover_id, crossover_direction):
        track_circuit_y_coord = track_circuit_id.split('-')[1]
        crossover_x_corrd = cls._get_connections_sorting_key(track_circuit_y_coord, crossover_id)
        comparison = None

        match crossover_direction:
            case '>': comparison = lambda x, y: x >= y
            case '<': comparison = lambda x, y: x <= y
        
        for index, neighbour_id in enumerate(neighbours):
            neighbours_x_coord = cls._get_connections_sorting_key(track_circuit_y_coord, neighbour_id)
            if comparison(neighbours_x_coord, crossover_x_corrd): return index


    @classmethod
    def _add_indexing(cls, crossover_id, crossover_direction, track_circuit_id):
        crossover_index = cls._get_index(Database.graph[track_circuit_id][crossover_direction], track_circuit_id, crossover_id, crossover_direction)
        Database.graph[crossover_id][crossover_direction][0] = track_circuit_id + f":{crossover_index}"
    

    @classmethod
    def _add_indexing_to_crossovers(cls):
        # every form of connection will be in the form of ID:index
        # thus knowing exactly which index to start getting neigbours from

        for crossover_id in Database.get_all_ids('CO'):
            for crossover_direction in Database.graph[crossover_id].keys():
                neighbours = Database.get_neighbours(crossover_id, crossover_direction)
                
                if neighbours == []: continue
                track_circuit_id = neighbours[0]
                cls._add_indexing(crossover_id, crossover_direction, track_circuit_id)


    @classmethod
    def _get_connections_sorting_key(self, curr_y_coordinate, component_id):
        component_details = component_id.split('-')
        id_prefix = component_details[0]
        key = None

        match id_prefix:
            case 'TC' : key = component_details[2]
            case 'CO' : 
                if curr_y_coordinate == component_details[1]: key = component_details[2]
                elif curr_y_coordinate == component_details[3]: key = component_details[4]

        return int(key)

    
    @classmethod
    def _reorder(cls, track_circuit_id):
        track_circuit_y_coordinate = track_circuit_id.split('-')[1]

        # reversing the order of left direction signals
        Database.all_signals[track_circuit_id]['<'].reverse()

        # the > direction connections should be sorted in increasing order of index
        Database.graph[track_circuit_id]['>'].sort(key=lambda id: cls._get_connections_sorting_key(track_circuit_y_coordinate, id))
        
        # the < direction connections should be sorted in decreasing order of index
        Database.graph[track_circuit_id]['<'].sort(key=lambda id: cls._get_connections_sorting_key(track_circuit_y_coordinate, id), reverse=True)



    # ------------------------------- classmethods to update visuals ------------------------------- #


    @classmethod
    def _finalize_all_components(cls):
        for component_type in Database.components_mapping.values():
            for component_id in getattr(Database, component_type):
                Database.get_component(component_id).finalize()


    @classmethod
    def _add_text_labels(cls):
        for field in constants.FIELD_TO_LABEL:
            for component_id in getattr(Database, field):
                component = Database.get_component(component_id)
                component.show_label()


    # ------------------------------- classmethods to generate tracks ------------------------------- #


    @classmethod
    def _generate_tracks(cls):
        # Future TODO (optimization)
        # An optimization method done to group all sequential single connectivity track circuits
        # for better/faster path finding and also to check intermediate positions in a path where
        # train can hault while fitting in a "track" without disturbing the traffic of network
        # or without making possibility of deadlocks
        
        # TRACKS + JUNCTIONS = COMPLETED MAP
        
        pass


    # ------------------------------ classmethods to generate junctions ------------------------------ #


    @classmethod
    def _generate_junctions(cls):
        # Future TODO (optimization)
        # any form of section which was not considered in tracks should be considered in junction
        # that is all those section which contains crosssovers
        
        # TRACKS + JUNCTIONS = COMPLETED MAP
        
        pass