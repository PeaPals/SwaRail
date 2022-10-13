# ------------------------------------- IMPORTING DEPENDENCIES ------------------------------------- #

# MAJOR TODO :- either make everything camel case or everything with underscore seperated (preffered _ seperated)


from SwaRail.config import SwaRailApplication
from SwaRail.Utilities import input_handler
from SwaRail.Utilities.timer import Timer
from SwaRail.Utilities.command_panel import CommandPanel


# ---------------------------------------- INITIALIZATIONS ---------------------------------------- #

CommandPanel.initialize()

def update():
    input_handler.check_navigations()
    Timer.update_time()  # TODO :- uncomment this when doing simulation


SwaRailApplication.run()