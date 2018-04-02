import random
from ingredients import ingredients_dict


status_dict = {
    'WAITING' : 0,
    'IN PROGRESS' : 1,
    'COMPLETED' : 2
}

class Order():
    def __init__(self, ingredients=None):
        self.status = status_dict['WAITING']
        self.ingredients = {}
        
        if ingredients:
            for ingredient in ingredients:
                if ingredient in ingredients_dict:
                    self.ingredients[ingredient] = 1
        else:
            for ingredient in ingredients_dict.keys():
                if random.random() > ingredients_dict[ingredient]['probability']:
                    self.ingredients[ingredient] = 1
        
                
    def get_remaining_ingredients(self):
        return [k for k,v in self.ingredients.iteritems() if v > 0]

    def process_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            self.ingredients[ingredient] -= 1

    def is_in_progress(self):
        return self.status == status_dict['IN PROGRESS']
        
    def set_status(self, status):
        if status in status_dict:
            self.status = status_dict[status]