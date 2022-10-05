from SwaRail.Frontend.MapHandler import parser
from SwaRail.database import Database


def load_map(map_name):
    # resetting saved database
    Database.reset_database()
    parser.MapParser.parse(map_name)