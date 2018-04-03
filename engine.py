## Engine class to represent full simulation engine
from futureEventList import FutureEventList
class Engine():
    def __init__(self, initial_events):
        self.current_time = -1
        self.future_event_list = FutureEventList()
        for e in initial_events:
            self.future_event_list.schedule(e)
        self.completed_event_list = []
        
    def schedule(self, event):
        self.future_event_list.schedule(event)

    def update(self, type, new_time):
        self.future_event_list.update( type, new_time)

    def update_order(self, order):
        self.future_event_list.update_order( order):
        
        
    def run(self): #function to execute next event in priority queue
        while self.future_event_list.len() > 0:
            next = self.future_event_list.pop(0)
            self.completed_event_list.append(next)
            self.current_time = next.ts
            next.callback(next.data)
            