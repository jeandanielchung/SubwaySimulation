import engine as eng
import random
from order import Order
from event import Event

NUM_ORDERS = 150
LAST_ORDER_TIME = 360 # time of last order (in minutes)

def main():
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
		new_event = Event(random.randint(0, LAST_ORDER_TIME), Order(), lambda x: 'Arrival Event') # TODO: replace with arrival event handler
		order_event_list.append(new_event)

	return order_event_list

if __name__ == "__main__":
    main()