class Station():
    def __init__(self, type, ingredients, time_to_process=lambda : 2):
        self.refill_delay = 5
        self.refill_quantity = 15
        self.time_to_process = time_to_process
        self.type = type
        self.time = 0
        self.ingredients = {}
        for ingredient in ingredients:
            self.ingredients[ingredient] = self.refill_quantity
    
    def update_time(self, time):
        self.time = time
    
    def process(self, order, time):
        """ processes an order by adding the station's ingredient """
        self.update_time(time)
        
        if len(order.get_remaining_ingredients_of_type(self.type)) == 0:
            return self.time
        
        delay = 0
        for ingredient in order.get_remaining_ingredients_of_type(self.type):
            if self.ingredients[ingredient] <= 0:
                delay += self.refill_delay
                self.ingredients[ingredient] = self.refill_quantity
            self.ingredients[ingredient] -= 1
            order.process_ingredient(ingredient)
        self.update_time(self.time + delay + self.time_to_process())
        return self.time