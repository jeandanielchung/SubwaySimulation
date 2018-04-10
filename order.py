import random
from ingredients import ingredients_dict
import sys

class Order():
    order_id = 0

    def __init__(self, start_time, ingredients=None):
        self.id = Order.order_id
        Order.order_id += 1
        self.ingredients = {}
        self.start_time = start_time
        self.completed_ts = sys.maxint
        self.wait_time = 0
        self.last_time_waiting = 0
        if ingredients:
            for ingredient in ingredients:
                if ingredient in ingredients_dict:
                    self.ingredients[ingredient] = 1
        else:
            for ingredient in ingredients_dict.keys():
                if random.random() <= ingredients_dict[ingredient]['probability']:

                    self.ingredients[ingredient] = 1
        
                
    def get_remaining_ingredients(self):
        """ gets the remaining ingredients to be added """
        return [k for k,v in self.ingredients.iteritems() if v > 0]
        
    def get_remaining_types(self):
        """ gets the remaining type of ingredients to be added """

        return list(set([ingredients_dict[k]['type'] for k,v in self.ingredients.iteritems() if v > 0]))

        
    def get_remaining_ingredients_of_type(self, type):
        """ gets remaining ingredients given a type """
        return [k for k,v in self.ingredients.iteritems() if ingredients_dict[k]['type'] == type and v > 0]

    def process_ingredient(self, ingredient):
        """ decrements the count of an ingredient """
        if ingredient in self.ingredients:
            self.ingredients[ingredient] -= 1
            
    def start_waiting(self, time):
        self.last_time_waiting = time
        
    def end_waiting(self, time):
        self.wait_time += time - self.last_time_waiting
    
    def __str__(self):
        return 'Order ' + str(self.id )+ ' with ' + str(self.ingredients)

