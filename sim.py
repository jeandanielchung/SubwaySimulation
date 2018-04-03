import engine as eng
import random
from order import Order
from event import Event
from station import Station
from ingredients import ingredients_dict, types
import json


engine = None
NUM_ORDERS = 7
LAST_ORDER_TIME = 360 # time of last order (in minutes)
NUM_PROCESSED = 0
done = 0

service_stations = {type : Station(type, [ingredient for ingredient,v in ingredients_dict.iteritems() if ingredients_dict[ingredient]['type'] == type]) for type in types}


def main():
    global engine
    # engine = eng.Engine(init_order_arrival_events(NUM_ORDERS))
    engine = eng.Engine(get_orders_from_file())
    start_time = engine.current_time
    engine.run()
    end_time = engine.current_time
    total_time = end_time - start_time

def get_orders_from_file():
    """function that gets the initial orders from a json file"""
    input_file = open("orders.json")
    x = json.load(input_file)
    orders = [Event(order["ts"], {'order' : Order(order["ts"], order["ingredients"]), 'time' : order["ts"], 'type' : 'ARRIVAL'}, 
        schedule_remaining_ingredients) for order in x["orders"]]
    NUM_ORDERS = len(orders)
    return orders
  
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
    """ starts adding a specified ingredient to an order and updates the FEL"""
    order = data['order']
    type = data['type']
    time = data['time']
    print 'Order ' + str(order.id) + ': start adding ingredient: ', type

    orderTime = service_stations[type].process(order, time)

    # print 'finished at time: ', orderTime

    engine.update(type, orderTime)
    

    schedule_remaining_ingredients({'order' : order, 'time' : orderTime})



def schedule_remaining_ingredients(data):
    """ updates the FEL and schedules the remaining ingredients to be added for an order"""
    global NUM_PROCESSED
    global done
    order = data['order']
    time = data['time']
    
    remTypes = order.get_remaining_types()
    engine.update_order(order)

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
        NUM_PROCESSED = NUM_PROCESSED + 1
        print 'Order ' + str(order.id) + ': finished sandwich at time: ' + str(time) + ' (time to process sandwich: ' + str(time - order.ts) + ')'
            
    if ((NUM_PROCESSED == NUM_ORDERS) and done == 0):
        print '----------------------------'
        print 'Number of orders processed: ' + str(NUM_PROCESSED)
        print 'Average time per sandwich ' + str(time / NUM_ORDERS)
        done = 1

if __name__ == "__main__":
    main()