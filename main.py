# ------------------------------------- IMPORTING DEPENDENCIES ------------------------------------- #

# MAJOR TODO :- either make everything camel case or everything with underscore seperated (preffered _ seperated)

from SwaRail.Frontend.MapHandler.MapLoader import load_map
from SwaRail.config import SwaRailApplication
from SwaRail.Utilities import InputHandler

# ---------------------------------------- INITIALIZATIONS ---------------------------------------- #

load_map("Section_B")



def update():
    InputHandler.check_navigations()


SwaRailApplication.run()