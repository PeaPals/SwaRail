from SwaRail.database import Database
from SwaRail.Frontend.MapHandler import load_map
import logging
from SwaRail import constants
from SwaRail.Simulator import Simulator

class CommandHandler:

    @classmethod
    def execute_command(cls, command: str):
        main_command = command.upper().strip().split(' ')

        match main_command:
            case ['LOADMAP', map_name]: load_map(map_name)
            case ['DIRECTIONMAP', state]: cls.toggle_direction_map(state)
            case ['STARTSIMULATION']: Simulator.start_simulation()
            # case ['ADDTRAIN', track_circuit_id, train_number]: cls.add_train_to_database(track_circuit_id, train_number)
            # case ['DELTRAIN', train_number]: cls.delete_train_from_database(train_number)
            # case ['REVIVETRACK', track_circuit_id]: cls.revive_track_circuit(track_circuit_id)
            # case ['REMOVETRACK', track_circuit_id]: cls.remove_track_circuit(track_circuit_id)
            case _: logging.warning(f'The entered command : "{command}" is invalid or cannot be executed at the moment')


    @staticmethod
    def toggle_direction_map(state):

        if state == 'ON':
            constants.TRACK_CIRCUIT_COLOR, constants.DIRECTIONMAP_TRACK_CIRCUIT_COLOR = (
                constants.DIRECTIONMAP_TRACK_CIRCUIT_COLOR, constants.TRACK_CIRCUIT_COLOR
            )