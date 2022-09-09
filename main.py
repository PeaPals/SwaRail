# ------------------------------------- IMPORTING DEPENDENCIES ------------------------------------- #

# MAJOR TODO :- either make everything camel case or everything with underscore seperated (preffered _ seperated)


from SwaRail.config import SwaRailApplication
from SwaRail.Utilities import input_handler
from SwaRail.Frontend import MapHandler


# ---------------------------------------- INITIALIZATIONS ---------------------------------------- #

MapHandler.load_map("Section_B")


def update():
    input_handler.check_navigations()


SwaRailApplication.run()