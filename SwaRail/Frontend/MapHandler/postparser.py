from SwaRail import constants

class PostParser():

    @classmethod
    def start_postparsing_operations(cls):
        cls._finalize_all_components()
        cls.summary()

    @classmethod
    def _finalize_all_components(cls):

        # TODO :- clean this code by using only 2 nested loops and __getattr__ function of Database class

        # finalize all track circuit
        for id, track_circuit in constants.Database.TRACK_CIRCUITS.items():
            track_circuit.finalize()
            # print(id, track_circuit)

        # finalize all haults
        for id, hault in constants.Database.HAULTS.items():
            hault.finalize()
            # print(id, hault)

        # finalize all signals
        for id, signal in constants.Database.SIGNALS.items():
            signal.finalize()
            # print(id, signal)

        # finalize all crossovers
        for id, crossover in constants.Database.CROSSOVERS.items():
            crossover.finalize()
            # print(id, crossover)

        # finalizing all seperators
        for id, seperator in constants.Database.SEPERATORS.items():
            seperator.finalize()
            # print(id, seperator)


    @classmethod
    def summary(cls):
        # logging a summary of database
        constants.logging.debug(constants.Database.summary())
