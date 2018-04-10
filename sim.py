import engine as eng
import random
from order import Order
from event import Event
from station import Station
from ingredients import ingredients_dict, types
import json
import copy
import numpy



engine = None
NUM_ORDERS = 10
LAST_ORDER_TIME = 100 # time of last order (in minutes)

SIMULTION_METHOD = 'ZIGZAG'


traditional_pipeline_order = ['ARRIVAL','MEAT', 'CHEESE', 'TOAST', 'VEG', 'SAUCE']

service_stations = None


def main():
    global engine
    global SIMULTION_METHOD
    global service_stations
    
    
    service_stations = {type : Station(type, [ingredient for ingredient,v in ingredients_dict.iteritems() if ingredients_dict[ingredient]['type'] == type], time_to_process=time_to_process) for type in types}
    initial_orders = init_order_arrival_events(NUM_ORDERS)
    initial_orders2 = copy.deepcopy(initial_orders)
    # initial_orders = get_orders_from_file()

    # print map(lambda x : str(x), initial_orders)
    for arrival in initial_orders:
        print str(arrival.data['order']) + ' at ' + str(arrival.data['order'].start_time)
        
    
    engine = eng.Engine(initial_orders)
    # engine = eng.Engine(get_orders_from_file())
    start_time = engine.current_time
    engine.run()
    end_time = engine.current_time
    zigzag_time = end_time - start_time
    
    print '----------------------------'
    print 'Number of orders processed: ' + str(len(engine.completed_orders))
    print 'Mean time per sandwich ' + str(zigzag_time / NUM_ORDERS)
    print 'Mean waiting time: ' + str(sum(map(lambda x: x.wait_time, engine.completed_orders)))
    print 'Standard deviation of wait times: ' + str(numpy.std(map(lambda x: x.wait_time, engine.completed_orders)))
    print engine.completed_orders
    
    
    service_stations = {type : Station(type, [ingredient for ingredient,v in ingredients_dict.iteritems() if ingredients_dict[ingredient]['type'] == type], time_to_process=time_to_process) for type in types}
    for arrival in initial_orders2:
        print str(arrival.data['order']) + ' at ' + str(arrival.data['order'].start_time)
    
    SIMULTION_METHOD = 'TRADITIONAL'
    engine = eng.Engine(initial_orders2)
    # engine = eng.Engine(get_orders_from_file())
    start_time = engine.current_time
    engine.run()
    end_time = engine.current_time
    traditional_time = end_time - start_time

    print '----------------------------'
    print 'Number of orders processed: ' + str(len(engine.completed_orders))
    print 'Mean time per sandwich ' + str(traditional_time / NUM_ORDERS)
    print "Mean waiting time: " + str(sum(map(lambda x: x.wait_time, engine.completed_orders)))
    print 'Standard deviation of wait times: ' + str(numpy.std(map(lambda x: x.wait_time, engine.completed_orders)))
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

def time_to_process():
    return int(numpy.random.normal(loc=3, scale=1))

def start_adding_ingredient(data):
    """ starts adding a specified ingredient to an order and updates the FEL"""
    order = data['order']
    type = data['event_type']
    time = data['event_time']
    # print 'Order ' + str(order.id) + ': start adding ingredient: ', type, ' at ', time

    order.end_waiting(time)
    
    completed_time = service_stations[type].process(order, time)

    # print 'finished at time: ', completed_time
    engine.update(type, completed_time)
    engine.update_order(order)

    if SIMULTION_METHOD is 'ZIGZAG':
        engine.schedule(Event({'order' : order, 
            'event_time' : completed_time, 'event_type' : 'END_' + type}, check_completed))
    else:
        schedule_remaining_ingredients({'order' : order, 
            'event_time' : completed_time, 'event_type' : type})
        
def check_completed(data):
    order = data['order']
    time = data['event_time']
    
    remTypes = order.get_remaining_types()
    
    if len(remTypes) == 0 and SIMULTION_METHOD is 'ZIGZAG':
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
    data['order'].start_waiting(data['event_time'])
    if SIMULTION_METHOD is 'ZIGZAG':
        schedule_remaining_ingredients_zig_zag(data)
    else:
        schedule_remaining_ingredients_pipeline(data)


def schedule_remaining_ingredients_pipeline(data):
    """ updates the FEL and schedules the remaining ingredients to be added for an order"""
    global NUM_PROCESSED
    global done
    order = data['order']
    time = data['event_time']
    type = data['event_type']
    
    remTypes = order.get_remaining_types()
    
    next_stage = traditional_pipeline_order.index(type) + 1
    data1 = copy.deepcopy(data)
    
    if next_stage < len(traditional_pipeline_order):
        data1['event_type'] = traditional_pipeline_order[next_stage]
        next_type = data1['event_type']
        if data1['event_time'] < service_stations[next_type].time:
            data1['event_time'] = service_stations[next_type].time
        
        engine.schedule(Event(data1, start_adding_ingredient))
    else:
        data1['event_type'] = 'COMPLETED'
        engine.schedule(Event(data1, complete_order))
   
    

def schedule_remaining_ingredients_zig_zag(data):
    """ updates the FEL and schedules the remaining ingredients to be added for an order"""
    order = data['order']
    
    remTypes = order.get_remaining_types()

    if 'TOAST' in remTypes:
        if 'MEAT' in remTypes:
            data1 = copy.deepcopy(data)
            data1['event_type'] = 'MEAT'
            if data['event_time'] < service_stations['MEAT'].time:
                data1['event_time'] = service_stations['MEAT'].time
            
            engine.schedule(Event(data1, start_adding_ingredient))

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