class Database:

    @classmethod
    def reset_database(cls):
        cls.TRACKS = {}
        cls.SIGNALS = {}
        cls.TRACK_CIRCUITS = {}
        cls.STATIONS = {}
        cls.HAULTS = {}


    @classmethod
    def summary(cls):
        return f'''
        TRACKS = {cls.TRACKS.keys()}\n
        TRACK CIRCUITS = {cls.TRACK_CIRCUITS.keys()}\n
        SIGNALS = {cls.SIGNALS.keys()}\n
        STATIONS = {cls.STATIONS}\n
        HAULTS = {cls.HAULTS.keys()}\n
        '''