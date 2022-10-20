# ------------------------------------- IMPORTING DEPENDENCIES ------------------------------------- #


from SwaRail import MapParser, SwaRailApplication, input_handler, Timer, CommandPanel


# ---------------------------------------- INITIALIZATIONS ---------------------------------------- #

MapParser.parse('Sonipat')

CommandPanel.initialize()

def update():
    input_handler.check_navigations()
    Timer.update_time()  # TODO :- uncomment this when doing simulation


SwaRailApplication.run()