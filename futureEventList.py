from ingredients import ingredients_dict, types
from sim import schedule_remaining_ingredients

class FutureEventList():
    def __init__(self):
        types.append('ARRIVAL')
        self.EventLists = {type: [] for type in types}


    def len(self):
        for type in types:
            if(len(self.EventLists[type]) != 0):
                return 1
        return 0

    def update(self, type, new_time):
        """function updating the queue for an ingredient type to delay events"""
        event_queue = self.EventLists[type]
        i = 0
        while i < len(event_queue) and new_time < event_queue[i].ts:
            event_queue[i] = new_time
            i += 1

    def update_order(self, order):
        """function update the new times of an order in each of the queues that it appears in"""
        for type in order.get_remaining_types():
            event_queue = self.EventLists[type]
            event_queue.remove(order)
            i = 0
            while i < len(event_queue) and new_time < event_queue[i].ts:
                i += 1
            event_queue.insert(Event(new_time, order, schedule_remaining_ingredients))

    def pop(self, i):
        min = float('inf')
        typePop = 'NULL'
        for type in types:
            if(len(self.EventLists[type]) != 0 and self.EventLists[type][0].ts < min):
                typePop = type
                min = self.EventLists[type][0].ts

        print 'Event type: ', typePop, 'At time: ', min


        return self.EventLists[typePop].pop(0)

    def schedule(self, event): #function to schedule event into priority queue (future event list)
        type = event.data['type']
        i =0
        while i < len(self.EventLists[type]):
            if self.EventLists[type][i].ts > event.ts:
                break
            i += 1
        self.EventLists[type].insert(i, event)



