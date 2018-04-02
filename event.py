## Event class to represent an event to be scheduled
class Event():
    def __init__(self, ts, data, callback):
        self.ts = ts
        self.data = data
        self.callback = callback

    def __str__(self):
        return 'Event with ' + str(self.data)