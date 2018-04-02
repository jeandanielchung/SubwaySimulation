

class Station():
    def __init__(self, type, ingredients, time_to_process=lambda x : 10):
        self.refill_delay = 10
        self.refill_quantity = 15
        self.type = type
        self.time = 0
        self.ingredients = {}
        for ingredient in ingredients:
            self.ingredients[ingredient] = self.refill_quantity
    
    def update_time(self, time):
        self.time = time
    
    def process(self, order):
        delay = 0
        for ingredient in order.get_remaining_ingredients_of_type(self.type):
            if self.ingredients[ingredient] <= 0:
                delay += self.refill_delay
                self.ingredients[ingredient] = self.refill_quantity
            self.ingredients[ingredient] -= 1
            order.process_ingredient(ingredient)
        self.update_time(self.time + delay + time_to_process())
        return self.time