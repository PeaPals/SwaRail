class Database:

    @classmethod
    def reset_database(cls):
        cls.TRACKS = {}
        cls.SIGNALS = {}
        cls.TRACK_CIRCUITS = {}
        cls.STATIONS = {}
        cls.HAULTS = {}
        cls.CROSSOVERS = {}
        cls.SEPERATORS = {}


    @classmethod
    def summary(cls):

        # for tc_id, tc in cls.TRACK_CIRCUITS.items():
        #     print(tc_id, tc)

        return f'''
        TRACKS = {cls.TRACKS.keys()}\n
        TRACK CIRCUITS = {cls.TRACK_CIRCUITS.keys()}\n
        SIGNALS = {cls.SIGNALS.keys()}\n
        STATIONS = {cls.STATIONS}\n
        HAULTS = {cls.HAULTS.keys()}\n
        CROSSOVERS = {cls.CROSSOVERS.keys()}\n
        SEPERATORS = {cls.SEPERATORS.keys()}\n
        '''