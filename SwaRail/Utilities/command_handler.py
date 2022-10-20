import logging
from SwaRail import settings
from SwaRail.database import Database

class CommandHandler:

    @classmethod
    def execute_command(cls, command: str):
        main_command = command.upper().strip().split(' ')

        match main_command:
            case ['LOADMAP', map_name]: from SwaRail import MapParser; MapParser.parse(map_name)
            case ['DIRECTIONMAP', state]: cls.toggle_direction_map(state)
            case ['S']: from SwaRail.Simulator import MainSimulator; simulator = MainSimulator()
            case ['REVIVETRACK', track_circuit_id]: cls.revive_track_circuit(track_circuit_id)
            case ['REMOVETRACK', track_circuit_id]: cls.remove_track_circuit(track_circuit_id)
            case _: logging.warning(f'The entered command : "{command}" is invalid or cannot be executed at the moment')



    @staticmethod
    def remove_track_circuit(track_circuit_id):
        node = Database.get_reference(track_circuit_id)
        
        if node == None:
            logging.info(f"Didn't found {track_circuit_id}")
            return None

        node.deactivate()
        logging.info(f"Deactivated {track_circuit_id}")

    @staticmethod
    def revive_track_circuit(track_circuit_id):
        node = Database.get_reference(track_circuit_id)
        
        if node == None:
            logging.info(f"Didn't found {track_circuit_id}")
            return None
        
        node.activate()
        logging.info(f"Activated {track_circuit_id}")



    @staticmethod
    def toggle_direction_map(state):

        if state == 'ON':
            settings.TRACK_CIRCUIT_COLOR, settings.DIRECTIONMAP_TRACK_CIRCUIT_COLOR = (
                settings.DIRECTIONMAP_TRACK_CIRCUIT_COLOR, settings.TRACK_CIRCUIT_COLOR
            )