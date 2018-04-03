from ingredients import ingredients_dict, types
from sim import schedule_remaining_ingredients

class FutureEventList():
    def __init__(self):
        types.insert(0,'ARRIVAL')
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
        while i < len(event_queue) and new_time >= event_queue[i].ts:
            event_queue[i].ts = new_time
            i += 1

    def update_order(self, order):
        """function to update the new times of an order in each of the queues that it appears in"""
        for type in order.get_remaining_types():
            event_queue = self.EventLists[type]
            self.EventLists[type] = list(filter(lambda x: x.data['order'].id != order.id, event_queue))

    def pop(self, i):
        """ pops the next event in the queue """
        min = float('inf')
        typePop = 'NULL'
        if len(self.EventLists['ARRIVAL']) != 0:
            print 'Event type: ARRIVAL', 'At time: ', self.EventLists['ARRIVAL'][0].ts
            return self.EventLists['ARRIVAL'].pop(0)
        for type in types:
            if(len(self.EventLists[type]) != 0 and self.EventLists[type][0].ts < min):
                typePop = type
                min = self.EventLists[type][0].ts
        order = self.EventLists[typePop][0].data['order']
        print 'Order ' + str(order.id) + ': Event type: ', typePop, 'At time: ', min


        return self.EventLists[typePop].pop(0)

    def schedule(self, event): 
        """ function to schedule event into priority queue (future event list) """
        type = event.data['type']
        i = 0
        while i < len(self.EventLists[type]):
            if self.EventLists[type][i].ts > event.ts:
                break
            i += 1
        self.EventLists[type].insert(i, event)



