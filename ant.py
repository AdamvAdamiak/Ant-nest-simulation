import random
import math
from nest import nest_worker
from food import food_worker


class Ant:
    def __init__(self, role, nest, food):
        self.food = food
        self.nest = nest
        self.x = 0
        self.y = 0
        self.speed = 4
        self.detect_food_radius = 25
        self.isLeavingNest = role
        self.hasFood = False
        self.FoodAmmount = 0

    def Update(self):
        if self.isLeavingNest == False:
            self.nest.food_stock -= 1
            return 0

        if self.hasFood == False:
            self.search_food()
        else:
            self.return_to_nest()

    def search_food(self):
        x_food, y_food = self.food.clossest_food(self.x, self.y)
        food_cords = (x_food, y_food)
        ant_cords = (self.x, self.y)

        # Jeśli wyczuje jedzenie, poruszam sie w jego kierunku
        if math.dist(ant_cords, food_cords) <= self.detect_food_radius:
            previous_dist = math.dist(ant_cords, food_cords)

            new_x = self.x
            new_y = self.y
            while True:

                if new_x < x_food:
                    new_x = self.x + random.randint(0, self.speed)
                else:
                    new_x = x_food

                if new_y < y_food:
                    new_y = self.y + random.randint(0, self.speed)
                else:
                    new_y = y_food

                ant_cords = (new_x, new_y)

                new_dist = math.dist(ant_cords, food_cords)

                if new_dist < previous_dist:
                    break

                if new_dist == 0:
                    self.grab_food(x_food, y_food)
                    break

            self.x = new_x
            self.y = new_y

            print(' x: ', self.x, ' y: ', self.y, ' dist: ',
                  math.dist(ant_cords, food_cords))
        else:
            # Jeśli nie wyczuje jedzenia ide w losowym kierunku
            self.x += random.randint(0, self.speed)
            self.y += random.randint(0, self.speed)
            print(' x: ', self.x, ' y: ', self.y, ' dist: ',
                  math.dist(ant_cords, food_cords))

    def grab_food(self, x_food, y_food):
        taken_food = self.food.take_from(x_food, y_food)
        self.FoodAmmount = taken_food
        self.hasFood = True

    def return_to_nest(self):
        nest_x, nest_y = self.nest.get_cords()

        if self.x != nest_x:
            if self.x > nest_x:
                self.x -= random.randint(0, self.speed)
            else:
                self.x += random.randint(0, self.speed)

        if self.y != nest_y:
            if self.y > nest_y:
                self.y -= random.randint(0, self.speed)
            else:
                self.y += random.randint(0, self.speed)

        if self.x == nest_x and self.y == nest_y:
            self.nest.food_stock += self.FoodAmmount
            self.FoodAmmount = 0
            self.hasFood = False

        print(' x: ', self.x, ' y: ', self.y, ' food: ', self.nest.food_stock)


f = food_worker
n = nest_worker
ant = Ant(True, n, f)


for i in range(500):
    ant.Update()
