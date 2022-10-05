#  TODO :-  what kind of heuristics should we consider so that most of the crossovers come near
# the destination station of the train


from SwaRail.Backend.Algorithms import PriorityQueue
from SwaRail.database import Database, State
from SwaRail.Utilities.mathematical import Vec2
from SwaRail import constants

# -------------------------------------- A* Helper Functions --------------------------------------- #


def id_to_coordinate(id) -> Vec2:
    prefix, x, y = id.split('-')
    return Vec2(int(x), int(y))


def coordinate_to_id(coordinate: Vec2) -> str:
    return f"TC-{coordinate.y}-{coordinate.x}"


def get_character_at_coordinate(coordinate: Vec2) -> str:
    return Database.get_railmap()[coordinate.y][coordinate.x]


# ------------------------------------- A* Neighbour Functions -------------------------------------- #

def verify_coordinate(coordinate: Vec2) -> bool:
    # will return wether or not the coordinate exist, and if it does it should not be a space
    return None


def get_crossover_neighbours(type: str, coordinate: Vec2) -> list[Vec2]:
    neighbours = [coordinate + Vec2(x=0, y=1)]

    match type:
        case '/': neighbours.append(coordinate + Vec2(x=1, y=-1))
        case '\\': neighbours.append(coordinate + Vec2(x=1, y=1))

    return neighbours



def get_neighbours(coordinate: Vec2, direction: str) -> Vec2:
    character = get_character_at_coordinate(coordinate)
    neighbours = None

    # starting check
    match character:
        case '-'|'=' : neighbours = [coordinate + Vec2(x=0, y=1)]
        # case '<'|'>': neighbours = [coordinate + Vec2(x=0, y=1)] if direction == character else []
        case '/'|'\\' : neighbours = get_crossover_neighbours(character, coordinate)
        case _ : neighbours = [coordinate + Vec2(x=0, y=1)]

    return verify_coordinate(neighbours)


# --------------------------------------- A* Major Functions --------------------------------------- #


def heuristics(current_coordinate, target_coordinate):
    return 0

    if current == '/':
        return Vec2.euclidian_distance(current_coordinate, target_coordinate)


def cost(current_coordinate, next_coordinate):
    return 0
    
    current_character = get_character_at_coordinate(current_coordinate)
    next_character = get_character_at_coordinate(next_coordinate)

    return constants.COST.get(f"{current_character}{next_coordinate}", 0)


def A_star_search(source : str, target : str, direction : str):
    source_coordinate = id_to_coordinate(source)
    target_coordinate = id_to_coordinate(target)

    came_from, cost_so_far = _A_Star(source_coordinate, target_coordinate, direction)
    character_path = reconstruct_character_path(came_from, source_coordinate, target_coordinate)
    # path = reconstruct_path_of_ids(character_path)

    print("Came From :", came_from)
    print("Cost So Far :", cost_so_far)
    print("Character path :", character_path)

    return None


def _A_Star(source_coordinate : Vec2, target_coordinate : Vec2, direction : str):
    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}
    
    frontier.put(source_coordinate, 0)
    came_from[source_coordinate] = 0
    cost_so_far[source_coordinate] = 0


    while not frontier.empty():
        current_coordinate = frontier.get()

        if current_coordinate == target_coordinate:
            break

        for next_coordinate in get_neighbours(current_coordinate, direction):
            if not Database.get_track_circuit_from_coordinates(next_coordinate).state == State.AVAILABLE:
                # MAJOR SECURITY TODO :- we are only checking wether the track circuit
                # is in Available state or not... I dont think there is a need to check wether crossover 
                # is available or not... But please make sure this doesn't end up as a major bug
                continue

            new_cost = cost_so_far[current_coordinate] + cost(current_coordinate, next_coordinate)

            if new_cost < cost_so_far.get(next_coordinate, float('inf')): # CRITICAL TODO :- look carefully where next will come or where next_id
                cost_so_far[next_coordinate] = new_cost
                priority = new_cost + heuristics(next_coordinate, target_coordinate)
                frontier.put(next_coordinate, priority)
                came_from[next_coordinate] = current_coordinate

    return came_from, cost_so_far


def reconstruct_character_path(came_from, source_coordinate, target_coordinate):
    if not target_coordinate in came_from:
        return []

    path = []
    current_coordinate = target_coordinate

    while current_coordinate != source_coordinate:
        path.append(get_character_at_coordinate(current_coordinate))
        current_coordinate = came_from[current_coordinate]
    
    path.append(get_character_at_coordinate(source_coordinate))
    path.reverse()
    
    return path


# def reconstruct_path_of_ids(coordinate_path: list[Vec2]):
#     id_path = []

#     for coordinate in coordinate_path:
