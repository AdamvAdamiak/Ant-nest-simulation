import random

class nest:

    def __init__(self,n):
        self.x = 0
        self.y = 0 
        self.food_stock = n

    def get_cords(self):
        return self.x,self.y

nest_worker = nest(50)