from SwaRail.Backend.BFS import connectivity_BFS
from SwaRail import Type, Database
import logging


    # --------------------------  class to handle post parsing operations --------------------------- #


class PostParser:

    @classmethod
    def start_postparsing_operations(cls) -> None:
        cls.finalize_references()
        cls.generate_connectivity_graph()
        cls.summary()


    @classmethod
    def finalize_references(cls) -> None:
        for ref_id, ref in Database.stream_references():
            if ref.type == Type.ANONYMOUS:
                continue

            ref.finalize_attributes()
            ref.draw()


    @classmethod
    def generate_connectivity_graph(cls) -> None:
        key_nodes = Database.get_all_hault_ids()

        for hault_id in key_nodes:
            for direction in ('>', '<'):
                connectivity_BFS(hault_id, direction, key_nodes)

        Database.calculate_connectivity_ratio(len(key_nodes))


    @classmethod
    def summary(cls):
        logging.info("parsing and post-parsing done successfully")
        Database.summary()