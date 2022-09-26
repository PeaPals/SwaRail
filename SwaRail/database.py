class Database:


    # def __getitem__(self, key):
    #     return self.A.get(key, "123")
    
    # def __class_getitem__(cls, key):
    #     return cls.A.get(key, "123")

    # def __setitem__(self, key, value):
    #     self.A[key] = value

    # def __delitem__(self, key):
    #     if self.A.get(key, False):
    #         del self.A[key]


    # tracks = {}
    # signals = {}
    # track_circuits = {}
    # stations = {}
    # haults = {}
    # crossovers = {}
    # seperators = {}

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

        return f'''
        TRACKS = {cls.TRACKS.keys()}\n
        TRACK CIRCUITS = {cls.TRACK_CIRCUITS.keys()}\n
        SIGNALS = {cls.SIGNALS.keys()}\n
        STATIONS = {cls.STATIONS}\n
        HAULTS = {cls.HAULTS.keys()}\n
        CROSSOVERS = {cls.CROSSOVERS.keys()}\n
        SEPERATORS = {cls.SEPERATORS.keys()}\n
        '''