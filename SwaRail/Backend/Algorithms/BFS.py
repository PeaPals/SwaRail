# Major TODO :- Use async BFS to find connectivity for each node to all other nodes
# To speed up the process and reduce some processing time

from queue import Queue
from SwaRail.database import Database


def connectivity_BFS(source : str, direction: str, key_nodes: set[str]):
    queue = Queue(maxsize=0)
    queue.put(source)
    visited = set()

    while not queue.empty():
        component_id = queue.get()
        component_true_id = component_id.split(":")[0]

        if component_id in visited:
            continue

        visited.add(component_id)

        if (component_true_id in key_nodes):
            Database.connectivity.add((source, component_true_id))
        
        # add all neighbours
        for neighbour_id in Database.get_neighbours(component_id, direction):
            if not neighbour_id in visited:
                queue.put(neighbour_id)
