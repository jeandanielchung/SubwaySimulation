import engine as eng
import random
from order import Order
from event import Event
from station import Station
from ingredients import ingredients_dict, types


engine = None
NUM_ORDERS = 150
LAST_ORDER_TIME = 360 # time of last order (in minutes)


service_stations = {type : Station(type, [ingredient for ingredient,v in ingredients_dict.iteritems() if ingredients_dict[ingredient]['type'] == type]) for type in types}


def main():
    global engine
    engine = eng.Engine(init_order_arrival_events(NUM_ORDERS))
    start_time = engine.current_time
    engine.run()
    end_time = engine.current_time
    total_time = end_time - start_time
  
def init_order_arrival_events(n):
    """ initialises and returns a list of order arrival events to process in the simulation engine
        (right now takes in just a parameter n, number of orders, but can take in distributions in the future) """ 
    order_event_list = []
    for i in range(n):
        time = random.randint(0, LAST_ORDER_TIME)
        new_event = Event(time, {'order' : Order(time), 'time' : time, 'type' : 'ARRIVAL'},   schedule_remaining_ingredients) 
        order_event_list.append(new_event)

    return order_event_list


def start_adding_ingredient(data):

    order = data['order']
    type = data['type']
    print 'start adding ingredient: ', type

    orderTime = service_stations[type].process(order)

    print 'finished at time: ', orderTime
    print order

    schedule_remaining_ingredients({'order' : order, 'time' : orderTime})



def schedule_remaining_ingredients(data):
    order = data['order']
    time = data['time']
    
    remTypes = order.get_remaining_types()

    #TODO: this needs to update the ts to time 
    #wherever this order appears in the list
    if 'TOAST' in remTypes:
        if 'MEAT' in remTypes:
            data['type'] = 'MEAT'
            engine.schedule(Event(time, data,   start_adding_ingredient))

        if 'CHEESE' in remTypes:
            data['type'] = 'CHEESE'
            engine.schedule(Event(time, data,   start_adding_ingredient))
        elif 'MEAT' not in remTypes:
            data['type'] = 'TOAST'
            engine.schedule(Event(time, data,   start_adding_ingredient))
    else:
        for type in remTypes:
            data['type'] = type
            engine.schedule(Event(time, data,   start_adding_ingredient))

    if len(remTypes) == 0:
        print 'Sandwich processed in ' + str(time - order.ts) + '!'
            


if __name__ == "__main__":
    main()