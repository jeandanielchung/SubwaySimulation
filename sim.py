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
		new_event = Event(random.randint(0, LAST_ORDER_TIME), Order(), lambda x: ScheduleRemainingIngredients) 
		order_event_list.append(new_event)

	return order_event_list




def startAddingMeat(order):

	orderTime = MeatStation.process(order)
	
	ScheduleRemainingIngredients(order, orderTime)

def startAddingCheese(order):

	orderTime = CheeseStation.process(order)
	
	ScheduleRemainingIngredients(order, orderTime)


def startAddingVeggie(order):

	orderTime = VeggieStation.process(order)
	
	ScheduleRemainingIngredients(order, orderTime)

def startAddingSauce(order):

	orderTime = SauceStation.process(order)
	
	ScheduleRemainingIngredients(order, orderTime)




def ScheduleRemainingIngredients(order, time):
	remIngredients = order.get_remaining_ingredients()
	#TODO: this needs to update the ts to time 
	#wherever this order appears in 
	if 'TOAST0' in remIngredients:
		if 'MEAT0' in remIngredients or 'MEAT1' in remIngredients:
			engine.schedule(Event(time, order, lambda x: startAddingMeat))

		if 'CHEESE0' in remIngredients or 'CHEESE1' in remIngredients:
			engine.schedule(Event(time, order, lambda x: startAddingCheese))
		elif 'MEAT0' not in remIngredients and 'MEAT1' not in remIngredients:
			engine.schedule(Event(time, order, lambda x: startAddingSauce))


	else:
		if 'MEAT0' in remIngredients or 'MEAT1' in remIngredients:
			engine.schedule(Event(time, order, lambda x: startAddingMeat))


		if 'CHEESE0' in remIngredients or 'CHEESE1' in remIngredients:
			engine.schedule(Event(time, order, lambda x: startAddingCheese))

		if 'VEGGIE0' in remIngredients or 'VEGGIE1' in remIngredients:
			engine.schedule(Event(time, order, lambda x: startAddingVeggie))


		if 'SAUCE0' in remIngredients or 'SAUCE1' in remIngredients:
			engine.schedule(Event(time, order, lambda x: startAddingSauce))








if __name__ == "__main__":
    main()