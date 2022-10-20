import logging



class Server:
    data = {}

    @classmethod
    def reset(cls):
        cls.data = {}

    @classmethod
    def add_train(cls, train_number, arriving_at_tc_id):
        cls.data[arriving_at_tc_id] = train_number


    @classmethod
    def get_train(cls, track_circuit_id):
        train = cls.data.pop(track_circuit_id, None)

        if train == None:
            logging.critical(f"Couldn't find train data from server present at {track_circuit_id}... SWITCH TO MANUAL")
            return None

        
        return train