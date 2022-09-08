from SwaRail.Frontend.MapHandler import RailMapLoader
from SwaRail import constants


def load_map(map_name):
    # resetting saved database
    constants.Database.reset_database()
    RailMapLoader.MapParser.parse(map_name)