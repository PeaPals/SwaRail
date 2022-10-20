# ------------------------------------- IMPORTING DEPENDENCIES ------------------------------------- #


from SwaRail import MapParser, SwaRailApplication, input_handler, Timer


# ---------------------------------------- INITIALIZATIONS ---------------------------------------- #

MapParser.parse('Sonipat')

# from SwaRail.Backend.path_finder import RouteProcessor, PathFinder

# main_route = ['SEC_B', 'SEC_C']
# print("Main Route :", main_route)
# route = RouteProcessor.process_route(main_route)
# print("Calculated Route :", route)
# path = PathFinder.find_path(route[0], route[1], direction='>')
# print("Calculated Path :", path)


def update():
    input_handler.check_navigations()
    Timer.update_time()  # TODO :- uncomment this when doing simulation


SwaRailApplication.run()