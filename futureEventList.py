from ingredients import ingredients_dict, types
class FutureEventList():
    def __init__(self):
        types.append('ARRIVAL')
        self.EventLists = {type: [] for type in types}



    def len(self):
        for type in types:
            if(len(self.EventLists[type]) != 0):
                return 1

        return 0

    def pop(self, i):
        min = float('inf')
        typePop = 'NULL'
        for type in types:
            if(len(self.EventLists[type]) != 0 and self.EventLists[type][0].ts < min):
                typePop = type
                min = self.EventLists[type][0].ts

        print 'Event type: ', typePop, 'At time: ', min

        return self.EventLists[typePop].pop(0)


        i =0
        while i < len(self.EventLists[type]):
            if self.EventLists[type][i].ts > event.ts:
                break
            i += 1
        self.EventLists[type].insert(i, event)



