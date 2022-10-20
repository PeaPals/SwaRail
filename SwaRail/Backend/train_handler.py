from .path_finder import PathFinder, RouteProcessor, PathHandler
from .priority_queue import PriorityQueue
from random import randint
from ursina import Entity
from SwaRail import settings, State

class _TrainHandler():
    def __init__(self):
        self.trains_queue = PriorityQueue()
        
        self.model = Entity()
        self.model.update = self.update
        self.time = settings.TRAIN_REPATH_COUNT_DOWN


    def add_train(self, number: str) -> None:
        self.trains_queue.put(number, randint(1, 10))

    def remove_train(self, number):
        self.trains_queue.elements.remove(number)
        self.reheapify_queue()


    def reheapify_queue(self):
        new_queue = []
        while not self.trains_queue.empty():
            new_queue.append(self.trains_queue.get())

        for ele in new_queue:
            self.trains_queue.put(ele)



    def update(self):
        if self.time != 0:
            self.time -= 1
            return None

        self.time = settings.TRAIN_REPATH_COUNT_DOWN

        from SwaRail import Database
        new_queue = []

        while not self.trains_queue.empty():
            train_number = self.trains_queue.get()
            train = Database.get_train(train_number)

            new_queue.append(train_number)

            if (train.route == [] or len(train.route) == 1):
                if train.path == None:
                    Database.remove_train(train.number)
                    new_queue.pop()
                    node_at = Database.get_reference(train.currently_at).state = State.AVAILABLE
                continue

            new_route = RouteProcessor.process_route(train.route.copy())
            if new_route == []: continue

            new_path = PathFinder.find_path(new_route[0], new_route[1], train.direction)
            if new_path == []: continue
            
            train.path = new_path
            PathHandler.book_path(new_path, train)




        for ele in new_queue:
            self.trains_queue.put(ele, randint(1, 10))



TrainHandler = _TrainHandler()