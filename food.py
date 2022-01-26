import random
import math
import numpy as np

class food:
    def __init__(self, n ):
        self.food_places = []
        self.n = n
        for i in range(n):
            x = random.randint(-64, 64)
            y = random.randint(-64, 64)
            self.food_places.append(food_object(x, y))

    def take_from(self, x, y, nest):
        for i in range(self.n):
            food_obj = self.food_places[i]
            if food_obj.x_food == x and food_obj.y_food == y:
                if food_obj.stock < 5:
                    stock = food_obj.stock
                    food_obj.stock = 0
                    food_obj.ants_visited
                    return stock
                food_obj.stock -= 5
                food_obj.ants_visited += 1
                food_obj.nest_visitors.append(nest.name)
                return 5

    def show(self):
        for k in self.food_places:
            print(k.x_food, k.y_food, k.stock)

    def clossest_food(self, x, y):
        distances = []
        visited = 0
        for food_obj in self.food_places:
            ant_cords = (x, y)
            food_cords = (food_obj.x_food, food_obj.y_food)
            # if int(food_obj.stock) == int(0):
            #     continue
            if food_obj.stock > 0:
                distances.append(math.dist(ant_cords, food_cords))
        
        clossest = min(distances)
        index = distances.index(clossest)
        clossest_food_obj = self.food_places[index]
        clossest_x = clossest_food_obj.x_food
        clossest_y = clossest_food_obj.y_food

        if clossest_food_obj.ants_visited > 0:
            visited = 1

        return clossest_x, clossest_y, visited

    def get_graph_data(self):
        x = []
        y = []
        stock = []
        visits = []
        for food_obj in self.food_places:
            x.append(food_obj.x_food)
            y.append(food_obj.y_food)
            stock.append(food_obj.stock)
            visits.append(food_obj.ants_visited)
        return x, y, stock, visits


    def stock_sum(self):
        a = 0
        for food_obj in self.food_places:
            a += food_obj.stock
        return a

class food_object:
    def __init__(self, x, y):
        self.x_food = x
        self.y_food = y
        self.stock = random.randint(5, 50)
        self.ants_visited = 0
        self.isEmpty = False
        self.nest_visitors = []
