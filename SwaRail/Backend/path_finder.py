from SwaRail.database import Database, State
from SwaRail.Backend.Algorithms import A_star_search
import logging   # Major TODO :- use logging everywhere using 'import logging' rather than constants of frontend



class RouteProcessor:

    @classmethod
    def process_route(cls, route):
        route = cls._convert_to_2d_route(route)
        route = cls._filter_connected_route(route)
        route = cls._convert_to_1d_route(route)

        return route


    @staticmethod
    def _convert_to_2d_route(route):
        for index, element in enumerate(route):
            if isinstance(element, list): continue

            all_haults = Database.stations.get(element, False)
            if all_haults == False: logging.critical(f"No station found for station ID :- {element}. Please switch back to manual mode as soon as possible")
            
            route[index] = all_haults

        return route


    @staticmethod
    def __get_platform_cost(platform_id):
        cost = 0
        cost += Database.get_component(platform_id).usage             # platform should be least used
        # cost += max(0, train.length - platform.length)              # platform should have enough length
                                                                      # to accomodate complete train

        return cost


    @classmethod
    def _get_platform(cls, platforms):
        # the platform should not be occupied
        platforms = filter(lambda platform : Database.get_component(platform).state == State.AVAILABLE, platforms)
        choosen_platform = min(platforms, key = lambda platform_id : cls.__get_platform_cost(platform_id))

        return choosen_platform


    @classmethod
    def _convert_to_1d_route(cls, route):
        # follow some rules to get the 1D path
        new_1d_path = []

        for platforms in route:
            track_circuit_id = cls._get_platform(platforms)

            if not track_circuit_id:  # TODO :- remove this
                return []

            new_1d_path.append(track_circuit_id)

        return new_1d_path


    @staticmethod
    def _get_filtered_next_layer(previous_layer, current_layer):
        new_current_layer = set()

        for previous_track_circuit_id in previous_layer:
            for current_track_circuit_id in current_layer:
                if (previous_track_circuit_id, current_track_circuit_id) in Database.connectivity:
                    new_current_layer.add(current_track_circuit_id)

        return new_current_layer


    @classmethod
    def _filter_connected_route(cls, route):
        new_path = [set(route[0])]

        for i in range(1, len(route)):
            previous_layer, current_layer = route[i-1], route[i]
            current_layer = cls._get_filtered_next_layer(previous_layer, current_layer)

            new_path.append(current_layer)

        return new_path




class PathFinder:
    
    @classmethod
    def find_path(cls, source, target):
        path = A_star_search(source, target, direction = '>')
        direction = '>'

        if not path:
            path = A_star_search(source, target, direction = '<')
            direction = '<'

        if path and cls.validate_path(path):
            return path, direction
        
        return False, False


    @staticmethod
    def validate_path(path):
        for node_id in path:
            if Database.get_component(node_id).state != State.AVAILABLE:
                return False

        return True