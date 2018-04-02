class futureEventList():

    def __init__(self):
        self.MeatEvents = []
        self.VegEvents = []
        self.CheeseEvents = []
        self.SauceEvents = []
        self.ToastEvents = []
        
        self.TYPE_DICT = {
            'MEAT':  self.MeatEvents,
            'VEG': self.VegEvents,
            'CHEESE': self.CheeseEvents,
            'SAUCE': self.SauceEvents,
            'TOAST': self.ToastEvents
        }



    def pop(self):
        min  = MeatEvents[0].ts
        eventList = 'MEAT'
        if(VegEvents[0].ts < min):
            eventList = 'VEG'
            min = VegEvents[0].ts
        if(CheeseEvents[0].ts < min):
            eventList = 'CHEESE'
            min = CheeseEvents[0].ts
        if(SauceEvents[0].ts < min):
            eventList = 'SAUCE'
            min = SauceEvents[0].ts
        if(ToastEvents[0].ts < min):
            eventList = 'TOAST'
            min = ToastEvents[0].ts
        
        if eventList == 'MEAT':
            return MeatEvents.pop(0)
        elif eventList == 'VEG':
             return VegEvents.pop(0)
        elif eventList == 'CHEESE':
             return CheeseEvents.pop(0)
        elif eventList == 'SAUCE':
             return SauceEvents.pop(0)
        elif eventList == 'TOAST':
             return ToastEvents.pop(0)


    def update(self, order, new_time):
        """function updating the queue for an ingredient type to delay events"""
        event_queue = TYPE_DICT[ingredient_type]
        i = 0
        while i < len(event_queue) and new_time < event_queue[i].ts:
            event_queue[i] = new_time
            i += 1


    def schedule(self, event):
        event_order = event.data
        for ingredient_type in event_order()
        event_queue = TYPE_DICT[ingredient_type]
        i =0
        while i < len(event_queue) and event.ts <= event_queue[i].ts:
            i += 1
        event_queue.insert(i, event)

    def schedule_meat(self, event): #function to schedule event into priority queue (future event list)
        i =0
        while i < len(self.MeatEvents):
            if self.MeatEvents[i].ts > event.ts:
                break
            i += 1
        self.MeatEvents.insert(i, event)

    def schedule_veg(self, event): #function to schedule event into priority queue (future event list)
        i =0
        while i < len(self.VegEvents):
            if self.VegEvents[i].ts > event.ts:
                break
            i += 1
        self.VegEvents.insert(i, event)    

    def schedule_cheese(self, event): #function to schedule event into priority queue (future event list)
        i =0
        while i < len(self.CheeseEvents):
            if self.CheeseEvents[i].ts > event.ts:
                break
            i += 1
        self.CheeseEvents.insert(i, event)

    def schedule_sauce(self, event): #function to schedule event into priority queue (future event list)
        i =0
        while i < len(self.SauceEvents):
            if self.SauceEvents[i].ts > event.ts:
                break
            i += 1
        self.SauceEvents.insert(i, event)

    def schedule_toast(self, event): #function to schedule event into priority queue (future event list)
        i =0
        while i < len(self.ToastEvents):
            if self.ToastEvents[i].ts > event.ts:
                break
            i += 1
        self.ToastEvents.insert(i, event)
