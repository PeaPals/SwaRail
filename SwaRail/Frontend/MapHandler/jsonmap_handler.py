import orjson as json
import constants as constants
# from Frontend.Components.tracks import Track


def load_jsonmap_data(map_name):
    try:
        map_data = json.loads(open(f"Data/Maps/{map_name}.json", 'rb').read())
    except FileNotFoundError as e:
        raise(e)

    return map_data