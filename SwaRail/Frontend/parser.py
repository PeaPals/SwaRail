from SwaRail.Components import Node
from SwaRail.Utilities import Vec2
from SwaRail import Type, Database, settings
from ursina import Vec3 as UrsinaVec3
from SwaRail.Frontend.postparser import PostParser
import logging


# Major TODO :- insert a special token @ to show connection between two different sections.
# It will represent the area connected by Automatic Block Signalling.

# Major TODO :- you removed most of the logging there was in parser... add them all back
# they were useful and important


class MapParser:
    map: list[list[str]] = None
    prev_node: Node = None
    curr_coords: Vec2 = Vec2(0, 0)



    @classmethod
    def parse(cls, map_name: str) -> None:
        cls._parse(map_name)
        PostParser.start_postparsing_operations()


    @classmethod
    def _parse(cls, map_name: str) -> None:
        cls.map = Database.load_railmap(map_name)

        # iterating through each line and parsing it
        for line_no, line in enumerate(cls.map):
            cls.curr_coords.y = line_no
            cls._parse_line(line)


    @classmethod
    def _parse_line(cls, line: list[str]) -> None:


        for index, character in enumerate(line):
            cls.curr_coords.x = index
            
            # starting check
            match character:
                case ' ': cls._end_curr_node()
                case '-' : continue
                case '/'|'\\': cls._check_token_validity(character)
                case '<'|'>'|'=' : cls._start_new_node(character, type=Type.TRACK)
                case 'X' : cls._start_new_node(character, type=Type.INTERSECTION)
                case '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9' : cls._add_new_signal(character)
                case _ : cls._update_station_id(character)


        # add any remaining component to the database
        if cls.prev_node != None:
            cls.curr_coords.x += 1
            cls._end_curr_node()


    # ------------------------- classmethods for general use by all methods ------------------------- #
    

    @classmethod
    def _get_id(cls, id_prefix: str = '', x: float = None, y: float = None) -> str:
        if x == None: x = cls.curr_coords.x
        if y == None: y = cls.curr_coords.y

        return f"{id_prefix}-{y}-{x}"


    @classmethod
    def _add_to_database(cls, node: Node) -> None:
        Database.add_node(node)


    @classmethod
    def _get_position(cls, x=None, y=None) -> Vec2:
        if x == None: x = cls.curr_coords.x
        if y == None: y = cls.curr_coords.y

        return UrsinaVec3(x, y, 0) * settings.MAP_MULTIPLIER


    @classmethod
    def _connect_nodes(cls, left_node: Node, right_node: Node) -> None:
        if left_node == None or right_node == None:
            return None

        left_node.add_neighbour(right_node.id, '>')
        right_node.add_neighbour(left_node.id, '<')


    @classmethod
    def _check_token_validity(cls, character: str) -> None:
        if character in ('/', '\\') and cls.prev_node != None:
            logging.critical(f"Found a crossover token at {cls.curr_coords} occuring during a active node connection; please replace this token with 'X' if required... and retry")
            raise Exception("CRITICAL_ERROR_WHILE_MAP_PARSING")


    # --------------------------------- classmethods related to nodes -------------------------------- #


    @classmethod
    def _start_new_node(cls, character: str, type: int):
        if type == Type.INTERSECTION and cls.prev_node == None:
            raise Exception("couldn't create intersection node if there is no prev node running")

        new_node = cls._create_new_node(character, type)

        match type:
            case Type.TRACK: cls._start_new_track_node(new_node)
            case Type.INTERSECTION: cls._start_new_intersection_node(new_node)


    @classmethod
    def _end_curr_node(cls):
        if cls.prev_node == None:
            return None

        anonymous_node = cls._create_new_node(direction='?', type=Type.ANONYMOUS)
        cls.prev_node.add_neighbour(anonymous_node.id, '>')
        cls.prev_node = None

        Database.add_node(anonymous_node)


    @classmethod
    def _create_new_node(cls, direction: str, type: int) -> Node:
        if type == Type.INTERSECTION or type == Type.ANONYMOUS:
            direction = cls.prev_node.direction

        return Node(
            id=cls._get_id('ND'), direction=direction, type=type, position=cls._get_position()
        )


    # -------------------------------- classmethods to update signals -------------------------------- #


    @classmethod
    def _add_new_signal(cls, character):
        pass

    @classmethod
    def _create_new_signal(cls, type):
        pass


    # ------------------------------ classmethods to update track nodes ----------------------------- #

    
    @classmethod
    def _start_new_track_node(cls, new_node: Node) -> None:
        cls._add_to_database(new_node)
        cls._connect_nodes(left_node=cls.prev_node, right_node=new_node)

        cls.prev_node = new_node


    # -------------------------- classmethods to update intersection nodes -------------------------- #

    @classmethod
    def _get_left_ending_node_id(cls, coords: Vec2) -> Vec2:
        coords = coords.copy() - Vec2(1, 1)
        
        while coords.y>=0 and coords.x>=0 and coords.x<len(cls.map[coords.y]):
            match cls.map[coords.y][coords.x]:
                case '\\': pass
                case 'X': return cls._get_id('ND', coords.x, coords.y)
                case _: return None

            coords -= Vec2(1, 1)

        return None

    @classmethod
    def _link_left_crossover(cls, curr_node: Node) -> None:
        left_node_id = cls._get_left_ending_node_id(cls.curr_coords)
        left_node = Database.get_node(left_node_id)
        cls._connect_nodes(left_node=left_node, right_node=curr_node)


    @classmethod
    def _get_right_ending_node_id(cls, coords: Vec2) -> Vec2:
        coords = coords.copy() - Vec2(-1, 1)
        
        while coords.y>=0 and coords.x>=0 and coords.x<len(cls.map[coords.y]):
            match cls.map[coords.y][coords.x]:
                case '/': pass
                case 'X': return cls._get_id('ND', coords.x, coords.y)
                case _: return None

            coords -= Vec2(-1, 1)
        
        return None

    @classmethod
    def _link_right_crossover(cls, curr_node: Node) -> None:
        right_node_id = cls._get_right_ending_node_id(cls.curr_coords)
        right_node = Database.get_node(right_node_id)
        cls._connect_nodes(left_node=curr_node, right_node=right_node)
    


    @classmethod
    def _start_new_intersection_node(cls, new_node: Node) -> None:
        cls._link_left_crossover(new_node)
        cls._link_right_crossover(new_node)
        cls._start_new_track_node(new_node)


    # ------------------------------- classmethods to update stations ------------------------------- #


    @classmethod
    def _update_station_id(cls, character: str):
        cls.prev_node.station_id += character