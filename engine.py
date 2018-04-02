
## Event class to represent an event to be scheduled
class Event():
    def __init__(self, ts, data, callback):
        self.ts = ts
        self.data = data
        self.callback = callback

## Engine class to represent full simulation engine
class Engine():
    def __init__(self):
        self.current_time = -1
        self.future_event_list = []
        self.completed_event_list = []
        
    def schedule(self, event): #function to schedule event into priority queue (future event list)
        i = 0
        while i < len(self.future_event_list):
            if self.future_event_list[i].ts > event.ts:
                break
            i += 1
        self.future_event_list.insert(i, event)
        
    def run(self): #function to execute next event in priority queue
        while len(self.future_event_list) > 0:
            next = self.future_event_list.pop(0)
            self.completed_event_list.append(next)
            self.current_time = next.ts
            next.callback(next.data)
            