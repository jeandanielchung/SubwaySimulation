import engine as eng
import random
from order import Order
from event import Event
from station import Station
from ingredients import ingredients_dict, types
import json
import copy


engine = None
NUM_ORDERS = 3
LAST_ORDER_TIME = 60 # time of last order (in minutes)

service_stations = {type : Station(type, [ingredient for ingredient,v in ingredients_dict.iteritems() if ingredients_dict[ingredient]['type'] == type]) for type in types}


def main():
    global engine
    # initial_orders = init_order_arrival_events(NUM_ORDERS)
    initial_orders = get_orders_from_file()

    # print map(lambda x : str(x), initial_orders)
    for arrival in initial_orders:
        print str(arrival.data['order']) + ' at ' + str(arrival.data['order'].start_time)
    engine = eng.Engine(initial_orders)
    # engine = eng.Engine(get_orders_from_file())
    start_time = engine.current_time
    engine.run()
    end_time = engine.current_time
    total_time = end_time - start_time

    print '----------------------------'
    print 'Number of orders processed: ' + str(len(engine.completed_orders))
    print 'Average time per sandwich ' + str(total_time / NUM_ORDERS)
    # print "average finishing time: " + str(sum(map(lambda x: x.completed_ts, engine.completed_orders))/len(engine.completed_orders))
    print engine.completed_orders

def get_orders_from_file():
    """function that gets the initial orders from a json file"""
    global NUM_ORDERS
    input_file = open("test_orders.json")
    x = json.load(input_file)
    orders = [Event({'order' : Order(order["ts"], order["ingredients"]), 
        'event_time' : order["ts"], 'event_type' : 'ARRIVAL'}, 
        check_completed) for order in x["orders"]]
    NUM_ORDERS = len(orders)
    return orders
  
def init_order_arrival_events(n):
    """ initialises and returns a list of order arrival events to process in the simulation engine
        (right now takes in just a parameter n, number of orders, but can take in distributions in the future) """ 
    order_event_list = []
    for i in range(n):
        time = random.randint(0, LAST_ORDER_TIME)
        new_event = Event({'order' : Order(time), 'event_time' : time, 'event_type' : 'ARRIVAL'},   check_completed) 
        order_event_list.append(new_event)

    return order_event_list


def start_adding_ingredient(data):
    """ starts adding a specified ingredient to an order and updates the FEL"""
    order = data['order']
    type = data['event_type']
    time = data['event_time']
    # print 'Order ' + str(order.id) + ': start adding ingredient: ', type, ' at ', time

    completed_time = service_stations[type].process(order, time)

    # print 'finished at time: ', completed_time
    engine.update(type, completed_time)
    engine.update_order(order)

    engine.schedule(Event({'order' : order, 
        'event_time' : completed_time, 'event_type' : 'END_' + type}, check_completed))

def check_completed(data):

    order = data['order']
    time = data['event_time']
    
    remTypes = order.get_remaining_types()

    if len(remTypes) == 0:
        engine.schedule(Event({'order' : order, 
        'event_time' : time, 'event_type' : 'COMPLETED'}, complete_order))
    else:
        schedule_remaining_ingredients(data)
   


def complete_order(data):
    order = data['order']
    time = data['event_time']

    # print 'Order ' + str(order.id) + ': finished sandwich at time: ' + str(time) + ' (time to process sandwich: ' + str(time - order.ts) + ')'
    order.completed_ts = time
    engine.completed_orders.append(order)




def schedule_remaining_ingredients(data):
    """ updates the FEL and schedules the remaining ingredients to be added for an order"""
    order = data['order']
    
    remTypes = order.get_remaining_types()

    if 'TOAST' in remTypes:
        if 'MEAT' in remTypes:
            data1 = copy.deepcopy(data)
            data1['event_type'] = 'MEAT'
            if data['event_time'] < service_stations['MEAT'].time:
                data1['event_time'] = service_stations['MEAT'].time
            
            engine.schedule(Event(data1,   start_adding_ingredient))

        if 'CHEESE' in remTypes:
            data1 = copy.deepcopy(data)
            data1['event_type'] = 'CHEESE'
            if data['event_time'] < service_stations['CHEESE'].time:
                data1['event_time'] = service_stations['CHEESE'].time
            engine.schedule(Event(data1,   start_adding_ingredient))
        elif 'MEAT' not in remTypes:
            data1 = copy.deepcopy(data)
            data1['event_type'] = 'TOAST'
            if data['event_time'] < service_stations['TOAST'].time:
                data1['event_time'] = service_stations['TOAST'].time
            engine.schedule(Event(data1,   start_adding_ingredient))
    else:
        for type in remTypes:
            data1 = copy.deepcopy(data)
            data1['event_type'] = type
            if data['event_time'] < service_stations[type].time:
                data1['event_time'] = service_stations[type].time
            engine.schedule(Event(data1,   start_adding_ingredient))

if __name__ == "__main__":
    main()