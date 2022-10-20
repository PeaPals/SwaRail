from SwaRail import State
from SwaRail.database import Database
from .A_star import A_star_search
import logging
from queue import Queue



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

            all_haults = list(Database.get_haults(element))
            
            if all_haults == []:
                logging.critical(f"No station found for station ID :- {element}. Please switch back to manual mode as soon as possible")
                return []
            
            route[index] = all_haults

        return route


    @staticmethod
    def __get_platform_cost(platform_id):
        cost = 0
        cost += Database.get_reference(platform_id).usage             # platform should be least used
        # cost += max(0, train.length - platform.length)              # TODO:- platform should have enough length
                                                                      # to accomodate complete train

        return cost


    @classmethod
    def _get_choosen_platform(cls, platforms):
        # the platform should not be occupied
        # TODO :- maybe problem here ?
        platforms = list(filter(lambda platform_id : Database.get_reference(platform_id).state == State.AVAILABLE, platforms))
        if len(platforms) == 0: return None

        # Major TODO :- should we alos check here if is any currently path available to platforms and
        # filter those platforms?

        choosen_platform = min(platforms, key = lambda platform_id : cls.__get_platform_cost(platform_id))
        return choosen_platform


    @classmethod
    def _convert_to_1d_route(cls, route):
        new_1d_path = [route[0][0]]

        for index in range(1, len(route)):
            platforms = route[index]
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

            route[index+1] = list(new_next_layer)

        return route

    
    @staticmethod
    def _filter_backwards(route):
        for index in range(len(route)-1, 0, -1):
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

            route[index-1] = list(new_prev_layer)

        return route



    @classmethod
    def _filter_connected_route(cls, route):
        sub_graph = cls._filter_backwards(route)
        sub_graph = cls._filter_forwards(sub_graph)
        
        return sub_graph




class PathHandler:
    
    @classmethod
    def book_path(cls, path, train):

        signal_seq = []
        train_color = Database.get_next_train_color()
        train.signal_seq = Queue(maxsize=0)


        for node_id in path:
            node = Database.get_reference(node_id)
            node.book(train.number, train_color)

            for signal_id in node.get_all_signals(train.direction):
                signal_seq.append(State.GREEN)




        _flag = False

        match len(signal_seq):
            case 0: pass
            case 1: signal_seq = [State.YELLOW]*1
            case 2: signal_seq = [State.YELLOW]*2
            case 3: signal_seq = [State.YELLOW]*3
            case _: _flag = True

        
        if _flag:
            signal_seq[-1] = State.YELLOW
            signal_seq[-2] = State.YELLOW
            signal_seq[-3] = State.YELLOW


        signal_seq.append(State.YELLOW)

        for state in signal_seq:
            train.signal_seq.put(state)

        cls.notify_track(path[0], train)
        cls.notify_track(path[1], train)


    @classmethod
    def notify_track(cls, node_id, train):
        node = Database.get_reference(node_id)
        node.notification(train)





class PathFinder:
    
    @classmethod
    def find_path(cls, source, target, direction):
        path = A_star_search(source, target, direction)
        return path