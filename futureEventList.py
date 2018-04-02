class futureEventList():
    def __init__(self):
        self.MeatEvents = []
        self.VegEvents = []
        self.CheeseEvents = []
        self.SauceEvents = []
        self.ToastEvents = []


    def schedule_meat(self, event): #function to schedule event into priority queue (future event list)
        i = 0
        while i < len(self.MeatEvents):
            if self.MeatEvents[i].ts > event.ts:
                break
            i += 1
        self.MeatEvents.insert(i, event)

    def schedule_veg(self, event): #function to schedule event into priority queue (future event list)
        i = 0
        while i < len(self.VegEvents):
            if self.VegEvents[i].ts > event.ts:
                break
            i += 1
        self.VegEvents.insert(i, event)    

    def schedule_cheese(self, event): #function to schedule event into priority queue (future event list)
        i = 0
        while i < len(self.CheeseEvents):
            if self.CheeseEvents[i].ts > event.ts:
                break
            i += 1
        self.CheeseEvents.insert(i, event)

    def schedule_sauce(self, event): #function to schedule event into priority queue (future event list)
        i = 0
        while i < len(self.SauceEvents):
            if self.SauceEvents[i].ts > event.ts:
                break
            i += 1
        self.SauceEvents.insert(i, event)

    def schedule_toast(self, event): #function to schedule event into priority queue (future event list)
        i = 0
        while i < len(self.ToastEvents):
            if self.ToastEvents[i].ts > event.ts:
                break
            i += 1
        self.ToastEvents.insert(i, event)
