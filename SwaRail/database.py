from ursina import color
import itertools
from SwaRail import settings


class Database:

    __railmap = None
    __stations = {}
    __references = {}
    __connectivity = set()
    connectivity_ratio = 0

    __models = {}


    train_colors = itertools.cycle([
        color.orange, color.yellow, color.lime, color.green, color.turquoise, color.cyan, color.azure,
        color.blue, color.violet, color.magenta, color.pink, color.brown, color.olive, color.peach,
        color.gold, color.salmon
    ])


    # --------------------------- classmethods for dealing with components --------------------------- #


    @classmethod
    def add_node(cls, node):
        Database.__references[node.id] = node

    @classmethod
    def get_node(cls, node_id):
        return cls.__references.get(node_id, None)

    @classmethod
    def stream_references(cls):
        return ((_id, reference) for _id, reference in cls.__references.items())

    @classmethod
    def get_railmap(cls):
        return cls.__railmap

    @classmethod
    def load_railmap(cls, railmap_name):
        with open(settings.MAP_PATH(railmap_name), 'r') as map_file:
            cls.__railmap = map_file.read().split('\n') # TODO :- convert path to absolute path

        return cls.__railmap


    @classmethod
    def set_model(cls, left_id, right_id, model):
        cls.__models[(left_id, right_id)] = cls.__models[(right_id, left_id)] = model

    @classmethod
    def get_model(cls, left_id, right_id):
        cls.__models.get((left_id, right_id), None)

    @classmethod
    def add_connectivity(cls, _from, _to):
        cls.__connectivity.add((_from, _to))

    @classmethod
    def get_connectivity(cls, _from, _to):
        return (_from, _to) in cls.__connectivity


    # ----------------------- classmethods for dealing with stations / haults ----------------------- #


    @classmethod
    def add_hault(cls, station_id: str, node_id: str) -> None:
        haults = cls.__stations.get(station_id, set())
        haults.add(node_id)
        cls.__stations[station_id] = haults
        
    @classmethod
    def get_haults(cls, station_id: str) -> list:
        return (hault_id for hault_id in cls.__stations.get(station_id, []))


    @classmethod
    def get_all_hault_ids(cls) -> list:
        all_haults = set()

        for station_id in cls.__stations.keys():
            all_haults = all_haults.union(cls.__stations[station_id])
        
        return all_haults


    @classmethod
    def calculate_connectivity_ratio(cls, total_key_nodes):
        ''' this will always be from 0 to 1 '''
        cls.connectivity_ratio = round(len(cls.__connectivity) / (total_key_nodes*(total_key_nodes-1)), 4)

    # -------------------------------------- other classmethods -------------------------------------- #


    @classmethod
    def reset_database(cls):
        cls.__railmap = None
        cls.__references = {}


    @classmethod
    def get_next_train_color(cls):
        return next(cls.train_colors)