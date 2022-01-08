import random


class nest:

    def __init__(self, n, k):
        self.x = 0
        self.y = 0
        self.food_stock = n
        self.ant_ammount = k

    def get_cords(self):
        return self.x, self.y
