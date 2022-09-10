class Database:

    @classmethod
    def reset_database(cls):
        cls.TRACKS = {}
        cls.SIGNALS = {}
        cls.TRACK_CIRCUITS = {}
        cls.STATIONS = {}
        cls.HAULTS = {}
        cls.CROSSOVERS = {}


    @classmethod
    def summary(cls):
        for track_circuit in cls.TRACK_CIRCUITS.values():
            print(f"{track_circuit.ID}, {track_circuit.connections}")
        

        return f'''
        TRACK_CIRCUITS = {cls.TRACK_CIRCUITS.keys()}
        '''

        return f'''
        TRACKS = {cls.TRACKS.keys()}\n
        TRACK CIRCUITS = {cls.TRACK_CIRCUITS.keys()}\n
        SIGNALS = {cls.SIGNALS.keys()}\n
        STATIONS = {cls.STATIONS}\n
        HAULTS = {cls.HAULTS.keys()}\n
        CROSSOVERS = {cls.CROSSOVERS.keys()}\n
        '''