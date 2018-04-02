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
        new_event = Event(random.randint(0, LAST_ORDER_TIME), Order(),   ScheduleRemainingIngredients) 
        order_event_list.append(new_event)

    return order_event_list




def startAddingMeat(order):

    orderTime = service_stations['MEAT'].process(order)
    
    ScheduleRemainingIngredients(order, orderTime)

def startAddingCheese(order):

    orderTime = service_stations['CHEESE'].process(order)
    
    ScheduleRemainingIngredients(order, orderTime)


def startAddingVeggie(order):

    orderTime = service_stations['VEG'].process(order)  
    
    ScheduleRemainingIngredients(order, orderTime)

def startAddingSauce(order):

    orderTime = service_stations['SAUCE'].process(order)
    
    ScheduleRemainingIngredients(order, orderTime)

def startToasting(order):
    orderTime = service_stations['TOAST'].process(order)
    ScheduleRemainingIngredients(order, orderTime)



def ScheduleRemainingIngredients(order, time):
    remTypes = order.get_remaining_types()
    #TODO: this needs to update the ts to time 
    #wherever this order appears in the list


    if 'TOAST' in remTypes:
        if 'MEAT' in remTypes:
            engine.schedule(Event(time, order,   startAddingMeat))

        if 'CHEESE' in remTypes:
            engine.schedule(Event(time, order,   startAddingCheese))
        elif 'MEAT' not in remTypes:
            engine.schedule(Event(time, order,   startToasting))


    else:
        if 'MEAT' in remTypes:
            engine.schedule(Event(time, order,   startAddingMeat))


        if 'CHEESE' in remTypes:
            engine.schedule(Event(time, order,   startAddingCheese))

        if 'VEGGIE' in remTypes:
            engine.schedule(Event(time, order,   startAddingVeggie))


        if 'SAUCE' in remTypes:
            engine.schedule(Event(time, order,   startAddingSauce))








if __name__ == "__main__":
    main()