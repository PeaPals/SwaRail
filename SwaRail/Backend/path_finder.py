from SwaRail import Database, State
from SwaRail.Backend.A_star import A_star_search
import logging



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
            if isinstance(element, list) or isinstance(element, set): continue

            all_haults = Database.get_haults(element, False)
            
            if all_haults == False:
                logging.critical(f"No station found for station ID :- {element}. Please switch back to manual mode as soon as possible")
                return []
            
            route[index] = all_haults

        return route


    @staticmethod
    def __get_platform_cost(platform_id):
        cost = 0
        cost += Database.get_node(platform_id).usage             # platform should be least used
        # cost += max(0, train.length - platform.length)              # TODO:- platform should have enough length
                                                                      # to accomodate complete train

        return cost


    @classmethod
    def _get_choosen_platform(cls, platforms):
        # the platform should not be occupied
        platforms = list(filter(lambda platform_id : Database.get_node(platform_id).state == State.AVAILABLE, platforms))
        if len(platforms) == 0: return None

        # Major TODO :- should we alos check here if is any currently path available to platforms and
        # filter those platforms?

        choosen_platform = min(platforms, key = lambda platform_id : cls.__get_platform_cost(platform_id))
        return choosen_platform


    @classmethod
    def _convert_to_1d_route(cls, route):
        # follow some rules to get the 1D path
        new_1d_path = []

        for platforms in route:
            choosen_platform = cls._get_choosen_platform(platforms)

            if choosen_platform == None:
                # no platform is available at the moment
                return []

            new_1d_path.append(choosen_platform)
        return new_1d_path


    @staticmethod
    def _filter_forwards(route):
        for index in range(len(route)-1):
            curr_layer = route[index]
            next_layer = route[index+1]
            new_next_layer = set()

            for curr_node_id in curr_layer:
                new_next_layer = new_next_layer.union(
                    filter(
                        lambda next_node_id: Database.get_connectivity(curr_node_id, next_node_id),
                        next_layer
                    )
                )

            route[index+1] = new_next_layer

    
    @staticmethod
    def _filter_backwards(route):
        for index in range(len(route), 0, -1):
            curr_layer = route[index]
            prev_layer = route[index-1]
            new_prev_layer = set()

            for curr_node_id in curr_layer:
                new_prev_layer = new_prev_layer.union(
                    filter(
                        lambda prev_node_id: Database.get_connectivity(prev_node_id, curr_node_id),
                        prev_layer
                    )
                )

            route[index-1] = new_prev_layer



    @classmethod
    def _filter_connected_route(cls, route):
        sub_graph = cls._filter_backwards(route)
        sub_graph = cls._filter_forwards(sub_graph)
        
        return sub_graph




class RouteHandler:

    @classmethod
    def book_route(cls, train_number, route):
        route = RouteProcessor.process_route(route)


    @classmethod
    def set_train_route(train_number, route):
        Database.add_route_to_train(train_number, route)







class PathFinder:
    
    @classmethod
    def find_path(cls, source, target, direction):
        path = A_star_search(source, target, direction)
        return path