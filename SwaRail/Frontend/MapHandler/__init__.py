from SwaRail.Frontend.MapHandler import railmap_handler
from SwaRail import constants


def load_map(map_name):
    # resetting saved database
    constants.Database.reset_database()
    railmap_handler.MapParser.parse(map_name)