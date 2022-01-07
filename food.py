import random
import math


class food:
    def __init__(self, n):
        self.food_places = []
        self.n = n
        for i in range(n):
            x = random.randint(12, 64)
            y = random.randint(12, 64)
            self.food_places.append(food_object(x, y))

    def take_from(self, x, y):
        for i in range(self.n):
            food_obj = self.food_places[i]
            if food_obj.x_food == x and food_obj.y_food == y:
                if food_obj.stock < 5:
                    stock = food_obj.stock
                    food_obj.stock = 0
                    return stock
                food_obj.stock -= 5
                return 5

    def show(self):
        for k in self.food_places:
            print(k.x_food, k.y_food, k.stock)

    def clossest_food(self, x, y):
        distances = []
        for i in range(self.n):
            food_obj = self.food_places[i]
            a = (x, y)
            b = (food_obj.x_food, food_obj.y_food)
            distances.append(math.dist(a, b))

        clossest = min(distances)
        index = distances.index(clossest)

        clossest_food_obj = self.food_places[index]
        clossest_x = clossest_food_obj.x_food
        clossest_y = clossest_food_obj.y_food

        return clossest_x, clossest_y


class food_object:
    def __init__(self, x, y):
        self.x_food = x
        self.y_food = y
        self.stock = random.randint(5, 50)


food_worker = food(5)
