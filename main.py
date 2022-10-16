# ------------------------------------- IMPORTING DEPENDENCIES ------------------------------------- #


from SwaRail import MapParser, SwaRailApplication
from SwaRail.Utilities import input_handler

# ---------------------------------------- INITIALIZATIONS ---------------------------------------- #

MapParser.parse('Sonipat')

def update():
    input_handler.check_navigations()
    # Timer.update_time()  # TODO :- uncomment this when doing simulation
    pass


SwaRailApplication.run()