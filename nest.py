import random


class nest:

    def __init__(self,name,x,y, n, k):
        self.x = x
        self.y = y
        self.food_stock = n
        self.ant_ammount = k
        self.name = name


    def get_cords(self):
        return self.x, self.y
