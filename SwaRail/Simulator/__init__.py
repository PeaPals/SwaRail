from SwaRail.Interface.backend_frontend import book_route



class Simulator:

    @classmethod
    def initialize(cls):
        cls.start_simulation()

    @classmethod
    def start_simulation(cls):
        # print(*Database.connectivity, sep='\n')
        # book_route(train_number="7")
        # book_route(train_number="3")
        # book_route(train_number="4")
        # book_route(train_number="1")
        # cls.summary()

        path = book_route(train_number="8")

        if next(path) or next(path):
            print("Path Generated")
        else:
            print("Will try again")

        pass