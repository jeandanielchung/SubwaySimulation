from ingredients import ingredients_dict, types
class FutureEventList():
    def __init__(self):
        self.EventLists = {type: [] for type in types}
        print self.EventLists


    def len(self):
        for type in types:
            if(len(EventLists[type]) != 0):
                return 1
        return 0

    def update(self, ingredient_type, new_time):
        """function updating the queue for an ingredient type to delay events"""
        event_queue = self.EventLists[ingredient_type]
        i = 0
        while i < len(event_queue) and new_time < event_queue[i].ts:
            event_queue[i] = new_time
            i += 1

    def pop(self, i):
        min = sys.intmax
        typePop = 'NULL'
        for type in types:
            if(len(EventLists[type]) != 0 and EventLists[type][0].ts < min):
                typePop = type
                min = EventLists[type][0].ts

        return EventLists[typePop].pop(0)


    def schedule(self, event, type): #function to schedule event into priority queue (future event list)
        i =0
        while i < len(self.EventLists[type]):
            if self.EventLists[type][i].ts > event.ts:
                break
            i += 1
        self.EventLists[type].insert(i, event)


