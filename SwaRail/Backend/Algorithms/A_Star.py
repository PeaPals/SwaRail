#  TODO :-  what kind of heuristics should we consider so that most of the crossovers come near
# the destination station of the train


from SwaRail.Backend.Algorithms import PriorityQueue
from SwaRail.database import Database, State
from SwaRail.Utilities import mathematical

# TODO :- optimize heuristics such that target does not keeps getting computed again and again
def heuristics(current_id, target_id):
    if current_id[:2] == 'TC':
        return 0
    
    # return 0

    current = Database.get_component(current_id)
    target = Database.get_component(target_id)

    current_mid_pos = (current.starting_pos + current.ending_pos) / 2
    target_mid_pos = (target.starting_pos + target.ending_pos) / 2

    print(mathematical.coordinate_distance(current_mid_pos, target_mid_pos, vec3=True) / 10)
    return mathematical.coordinate_distance(current_mid_pos, target_mid_pos, vec3=True) / 10


def cost(current_id, next_id):
    next_id_pefix = next_id[:2]

    match next_id_pefix:
        case 'TC' : return 1
        case 'CO' : return 1



def A_star_search(source : str, target : str, direction : str):
    came_from, cost_so_far = _A_Star(source, target, direction)
    path = reconstruct_path(came_from, source, target)

    print(path, came_from)

    return path


def _A_Star(source : str, target : str, direction : str):
    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}
    
    frontier.put(source, 0)
    came_from[source] = 0
    cost_so_far[source] = 0


    while not frontier.empty():

        print(frontier.elements)

        current = frontier.get()
        current_id = current.split(':')[0]

        if current_id == target:
            break

        for next in Database.get_neighbours(current, direction):
            next_id = next.split(':')[0]

            if not Database.state[next_id] == State.AVAILABLE:
                continue

            new_cost = cost_so_far[current_id] + cost(current_id, next_id)

            if new_cost < cost_so_far.get(next_id, float('inf')): # CRITICAL TODO :- look carefully where next will come or where next_id
                cost_so_far[next_id] = new_cost
                priority = new_cost + heuristics(next_id, target)
                frontier.put(next, priority)
                came_from[next_id] = current_id

    return came_from, cost_so_far


def reconstruct_path(came_from, source, target):
    if not target in came_from:
        return []

    path = []
    current = target
    while current != source:
        path.append(current)
        current = came_from[current]
    
    path.append(source)
    path.reverse()
    
    return path