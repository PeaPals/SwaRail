from SwaRail.Frontend.MapHandler import railmap_handler
from SwaRail.database import Database


def load_map(map_name):
    # resetting saved database
    Database.reset_database()
    railmap_handler.MapParser.parse(map_name)