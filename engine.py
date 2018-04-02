## Engine class to represent full simulation engine
import FutureEventList
class Engine():
    def __init__(self, initial_events):
        self.current_time = -1
        self.future_event_list = FutureEventList()
        for e in initial_events:
            self.future_event_list.schedule_arrival(e)
        self.completed_event_list = []
        

        
    def run(self): #function to execute next event in priority queue
        while len(self.future_event_list) > 0:
            next = self.future_event_list.pop(0)
            self.completed_event_list.append(next)
            self.current_time = next.ts
            next.callback(next.data)
            