from SwaRail.Frontend import constants
from SwaRail.database import Database

class PostParser():

    @classmethod
    def start_postparsing_operations(cls):
        
        # visual stuff
        cls._finalize_all_components()
        cls._add_text_labels()

        # generating optimized database to be used by backend
        cls._generate_tracks()
        cls._generate_junctions()

        # final summary
        cls.summary()


    # ------------------------------- classmethods for global use ------------------------------- #


    @classmethod
    def summary(cls):
        # logging a summary of database
        constants.logging.debug(Database.summary())


    # ------------------------------- classmethods to update text labels ------------------------------- #


    # MAJOR TODO :- add text labels to all track circuits ID... on them... maybe show them if zoomed in enough?

    @classmethod
    def _add_text_labels(cls):
        for field in constants.FIELD_TO_LABEL:
            for component in getattr(Database, field).values():
                component.show_label()


    # ------------------------------- classmethods to update visuals ------------------------------- #


    @classmethod
    def _finalize_all_components(cls):

        # TODO :- clean this code by using only 2 nested loops and __getattr__ function of Database class

        # finalize all track circuit
        for id, track_circuit in Database.TRACK_CIRCUITS.items():
            track_circuit.finalize()
            # print(id, track_circuit)

        # finalize all haults
        for id, hault in Database.HAULTS.items():
            hault.finalize()
            # print(id, hault)

        # finalize all signals
        for id, signal in Database.SIGNALS.items():
            signal.finalize()
            # print(id, signal)

        # finalize all crossovers
        for id, crossover in Database.CROSSOVERS.items():
            crossover.finalize()
            # print(id, crossover)

        # finalizing all seperators
        for id, seperator in Database.SEPERATORS.items():
            seperator.finalize()
            # print(id, seperator)


    # ------------------------------- classmethods to generate tracks ------------------------------- #


    @classmethod
    def _generate_tracks(cls):
        pass


    # ------------------------------ classmethods to generate junctions ------------------------------ #


    @classmethod
    def _generate_junctions(cls):
        pass
