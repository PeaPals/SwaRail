from SwaRail import State
from .priority_queue import PriorityQueue


# --------------------------------------- A* Major Functions --------------------------------------- #


#  TODO :-  what kind of heuristics should we consider so that most of the crossovers come near
# the destination station of the train


def heuristics(current_id, target_id):
    return 0


def cost(current_id, next_id):
    return 0


def A_star_search(source : str, target : str, direction : str):
    came_from, cost_so_far = _A_Star(source, target, direction)
    path = reconstruct_path(came_from, source, target)
    return path


def _A_Star(source : str, target : str, direction : str):
    from SwaRail import Database
    
    frontier = PriorityQueue()
    came_from = {}
    cost_so_far = {}
    
    frontier.put(source, 0)
    came_from[source] = 0
    cost_so_far[source] = 0


    while not frontier.empty():
        current_node_id = frontier.get()

        if current_node_id == target:
            break

        for next_node_id in Database.get_reference(current_node_id).get_neighbours(direction):
            next_node = Database.get_reference(next_node_id)

            if next_node.state != State.AVAILABLE:
                continue

            new_cost = cost_so_far[current_node_id] + cost(current_node_id, next_node_id)
            if new_cost < cost_so_far.get(next_node_id, float('inf')):
                cost_so_far[next_node_id] = new_cost
                priority = new_cost + heuristics(next_node_id, target)
                frontier.put(next_node_id, priority)
                came_from[next_node_id] = current_node_id


    return came_from, cost_so_far


def reconstruct_path(came_from, source, target):
    
    current = target
    path = []

    if target not in came_from:
        return []

    while current != source:
        path.append(current)
        current = came_from[current]

    path.append(source)
    path.reverse()

    return path