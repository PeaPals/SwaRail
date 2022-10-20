from SwaRail import settings
from ursina import color
import itertools
import logging


class Database:

    __railmap = None
    __stations = {}
    __trains = {}
    __references = {}
    __connectivity = set()
    connectivity_ratio = 0
    

    train_colors = itertools.cycle([
        color.orange, color.yellow, color.lime, color.green, color.turquoise, color.cyan, color.azure,
        color.blue, color.violet, color.magenta, color.pink, color.brown, color.olive, color.peach,
        color.gold, color.salmon
    ])


    # --------------------------- classmethods for dealing with components --------------------------- #


    @classmethod
    def add_reference(cls, ref):
        Database.__references[ref.id] = ref

    @classmethod
    def get_reference(cls, ref_id):
        return cls.__references.get(ref_id, None)

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
    def add_connectivity(cls, _from, _to):
        cls.__connectivity.add((_from, _to))

    @classmethod
    def get_connectivity(cls, _from, _to):
        return (_from, _to) in cls.__connectivity


    # ----------------------- classmethods for dealing with stations / haults ----------------------- #


    @classmethod
    def add_hault(cls, station_id: str, node_id: str) -> None:
        haults = cls.__stations.get(station_id, [])
        haults.append(node_id)
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


    # ------------------------------------ classmethods for trains ----------------------------------- #


    @classmethod
    def add_train(cls, train_number, train):
        from SwaRail import TrainHandler
        
        cls.__trains[train_number] = train
        TrainHandler.add_train(train_number)

    @classmethod
    def remove_train(cls, train_number):
        from SwaRail import TrainHandler

        cls.__trains.pop(train_number, None)
        TrainHandler.remove_train(train_number)


    @classmethod
    def get_train(cls, train_number):
        return cls.__trains.get(train_number, None)

    @classmethod
    def get_all_trains(cls):
        return (train for train in cls.__trains.values())


    # -------------------------------------- other classmethods -------------------------------------- #


    @classmethod
    def reset_database(cls):
        cls.__railmap = None
        cls.__references = {}


    @classmethod
    def get_next_train_color(cls):
        return next(cls.train_colors)


    @classmethod
    def summary(cls):
        logging.info(f"Connectivity ratio of this map is {cls.connectivity_ratio}")
        logging.info(f"There are {len(cls.__stations)} major hault groups detected")
        logging.info(f"There are {len(cls.__references)} present for this map")