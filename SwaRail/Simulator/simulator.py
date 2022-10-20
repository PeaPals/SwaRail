from ursina import Entity
from SwaRail import settings, Database, State
from SwaRail.Server import Server
from SwaRail.Components.train import Train
import orjson as json
from datetime import datetime, timedelta
import logging


class Simulator():

    def __init__(self):
        logging.info("Simulator turned on")
        self.data = None
        self.time = settings.TRAIN_POSITION_UPDATE_TIME
        self.start_simulation()
        
        self.model = Entity()
        self.model.update = self.update

    def load_simulation(self):
        with open('Data/Trains/route_data.json', 'rb') as f:
            self.data = json.loads(f.read())["routes"]

    def set_timings(self):
        for index, record in enumerate(self.data):
            hours, minutes, seconds = map(int, record["arriving_at"].split(':'))
            record["arriving_at"] = datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)
            self.data[index] = record


    def start_simulation(self):
        self.load_simulation()
        self.set_timings()


    def update(self):
        self.time -= 1

        if self.time == 0:
            self.update_train_positions()
            self.time = settings.TRAIN_POSITION_UPDATE_TIME

        if not self.data:
            return None

        for record in self.data:
            arriving_at = record["arriving_at"]

            if datetime.now() >= arriving_at:
                simulated = self.add_train_to_map(record)
                if simulated:
                    self.data.pop(0)
                    logging.info(f"Successfully added train number {record['train_number']} to simulation")




    def add_train_to_map(self, record) -> bool:
        train_number = record["train_number"]
        route = record["route"].copy()
        arriving_at_index = record["arriving_at_index"]
        direction = record["direction"]

        if len(route) == 0:
            raise Exception('EMPTY_ROUTE')

        starting_track_circuit = Database.get_reference(next(Database.get_haults(route[0])))
        if starting_track_circuit.state != State.AVAILABLE:
            return False

        self.send_train_data_to_server(train_number, starting_track_circuit.id)
        
        train = Train(number=train_number, route=route, direction=direction)
        Database.add_train(train_number, train)
        starting_track_circuit.state = State.OCCUPIED

        return True


    def send_train_data_to_server(self, train_number, arriving_at_tc_id):
        Server.add_train(train_number, arriving_at_tc_id)


    def update_train_positions(self):
        for train in Database.get_all_trains():

            if train.route == [] and train.path == None:
                last_tc_node = train.currently_at
                node = Database.get_reference(last_tc_node)
                node.state = State.AVAILABLE
                
                Database.remove_train(train.number)
                continue

            if train.path == None:
                continue

            if train.path == []:
                train.path = None
                continue


            curr_track_id = train.currently_at
            next_track_id = train.path[0]

            curr_track = Database.get_reference(curr_track_id)
            next_track = Database.get_reference(next_track_id)

            _flag = True
            for signal_id in curr_track.get_all_signals(train.direction):
                if Database.get_reference(signal_id).state == State.RED:
                    _flag = False
                    break
            # check here if all signals in curr_track is green or yellow (not red)... only then move forward

            if _flag:
                next_track.state = State.OCCUPIED
                curr_track.state = State.AVAILABLE
