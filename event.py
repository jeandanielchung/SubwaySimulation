## Event class to represent an event to be scheduled
class Event():
    def __init__(self, data, callback):
        self.data = data
        self.callback = callback

    def __str__(self):
        return str(self.data['event_type']) + ' event at ' + str(self.data['event_time']) + ': ' + str(self.data['order'])