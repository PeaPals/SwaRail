from ursina import color
import itertools

class State:
    AVAILABLE = 0
    BOOKED = 1
    OCCUPIED = 2


class Database:


    # def __getitem__(self, key):
    #     return self.A.get(key, "123")
    
    # def __class_getitem__(cls, key):
    #     return cls.A.get(key, "123")

    # def __setitem__(self, key, value):
    #     self.A[key] = value

    # def __delitem__(self, key):
    #     if self.A.get(key, False):
    #         del self.A[key]


    # TODO :- make a feature inside database class such that writing
    # Database[component.ID] = component will automatically insert it to the right place
    # and same for retrieval of data


    railmap : list[str] = None
    
    graph : dict[str, dict[str, list[str]]] = {}
    state : dict[str, int] = {}
    stations : dict[str, set[str]] = {}
    all_signals : dict[str, dict[str, list[str]]] = {}
    connectivity = set()

    usage = {}

    train_colors = [
        color.orange, color.yellow, color.lime, color.green, color.turquoise, color.cyan, color.azure,
        color.blue, color.violet, color.magenta, color.pink, color.brown, color.olive, color.peach,
        color.gold, color.salmon
    ]

    train_color_generator = itertools.cycle(train_colors)
    

    components_mapping = {
        "TC" : "track_circuits",
        "SI" : "signals",
        "CO" : "crossover",
        "SP" : "seperators"
    }


    __references = {}


    # --------------------------- classmethods for dealing with components --------------------------- #


    @classmethod
    def add_component(cls, component):
        id_prefix = component.ID[:2]
        component_type = cls.components_mapping.get(id_prefix, False)

        if component_type:
            getattr(cls, component_type).add(component.ID)
            cls.__references[component.ID] = component


    @classmethod
    def get_component(cls, component_id):
        return cls.__references.get(component_id, None)


    @classmethod
    def get_all_ids(cls, component_prefix):
        component_name = cls.components_mapping.get(component_prefix, None)

        match component_name:
            case None: return set()
            case _: return getattr(cls, component_name)


    @classmethod
    def get_neighbours(cls, id, direction):
        details = id.split(":")
        
        match len(details):
            case 1: id, index = id, 0
            case 2: id, index = details[0], int(details[1])

        component_connections = cls.graph.get(id, {'<': [], '>': []})
        return component_connections[direction][index:]


    # ----------------------- classmethods for dealing with stations / haults ----------------------- #


    @classmethod
    def add_hault(cls, station_id, track_circuit_id):
        all_platforms = cls.stations.get(station_id, [])
        all_platforms.append(track_circuit_id)
        cls.stations[station_id] = all_platforms

    @classmethod
    def get_all_haults(cls):
        all_haults = set()

        for station_id in cls.stations.keys():
            for track_circuit_id in cls.stations[station_id]:
                all_haults.add(track_circuit_id)

        return all_haults


    # ----------------------------- classmethods for dealing with graph ----------------------------- #


    @classmethod
    def register_graph_node(cls, component):
        id_prefix = component.ID[:2]
        
        match id_prefix:
            case 'TC' : cls.all_signals[component.ID] = {'>': [], '<' : []}

        cls.graph[component.ID] = {'>': [], '<' : []}
        cls.state[component.ID] = State.AVAILABLE



    @classmethod
    def add_graph_connection(cls, left_component, right_component):
        cls.graph[left_component.ID]['>'].append(right_component.ID)
        cls.graph[right_component.ID]['<'].append(left_component.ID)


    @classmethod
    def bind_signal_to_track_circuit(cls, track_circuit, signal):
        cls.all_signals[track_circuit.ID][signal.direction].append(signal.ID)


    # -------------------------------------- other classmethods -------------------------------------- #


    @classmethod
    def reset_database(cls):
        for component_type in cls.components_mapping.values():
            setattr(cls, component_type, set())


    @classmethod
    def get_next_train_color(cls):
        return next(cls.train_color_generator)
        

    @classmethod
    def summary(cls):
        summary = ["Database Summary : "]
        
        for component_type in cls.components_mapping.values():
            summary.append(f"\n{component_type} = {getattr(cls, component_type)}")

        summary.append(f"\nStations : {cls.stations}")

        cls.printer() # TODO :- remove this

        return '\n'.join(summary)


    # TODO :  remove this
    @classmethod
    def printer(cls):
        
        import pprint
        print("Database connections : ")
        print("\n\nGraph : ")
        pprint.pprint(cls.graph)
        # print(cls.graph)
        print("\n\nSignals : ")
        pprint.pprint(cls.all_signals)
        # print(cls.all_signals)