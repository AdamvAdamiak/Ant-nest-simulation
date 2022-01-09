import random
import math
from math import fabs

class Ant:
    def __init__(self, role, nest, food):
        self.food = food
        self.nest = nest
        self.x = 0
        self.y = 0
        self.speed = 5
        self.detect_food_radius = 5000
        self.isLeavingNest = role
        self.hasFood = False
        self.FoodAmmount = 0
        self.DeathTimer = 10
        self.isDead = False
        self.stickToCord = 0
        self.x_food = 0
        self.y_food = 0

    def Update(self):
        if self.isLeavingNest == True:
            if self.nest.food_stock <= 0:
                self.DeathTimer -= 1

        if random.randint(0,10000) < 5 or self.DeathTimer == 0:
            self.isDead = True

        if self.x > 64 or self.x < -64 or self.y > 64 or self.y < -64:
            print('XD?')
            self.return_to_nest()

        if self.isDead == True:
            return 'dead'

        if self.isLeavingNest == False:
           return self.check_for_staying_ant()

        if self.hasFood == False:
            return self.search_food()
        else:
            if self.FoodAmmount > 0:
                self.FoodAmmount -= 0.01
            return self.return_to_nest()

    def check_for_staying_ant(self):
        if self.nest.food_stock <= 0:
            self.DeathTimer -= 1
        else:
            self.nest.food_stock -= 0.01
            self.DeathTimer = 10
        if self.DeathTimer == 0:
            self.isDead = True
            return 'dead'
        return 'alive'

    def search_food(self):
        if self.stickToCord == 0:
            try:
                self.x_food, self.y_food = self.food.clossest_food(self.x, self.y)
                self.stickToCord = 25
            except ValueError: 
                return 'alive'
        self.stickToCord -= 1
        food_cords = (self.x_food, self.y_food)
        ant_cords = (self.x, self.y)

        # Jeśli wyczuje jedzenie, poruszam sie w jego kierunku
        if math.dist(ant_cords, food_cords) <= self.detect_food_radius:
            previous_dist = math.dist(ant_cords, food_cords)
            new_x = self.x
            new_y = self.y
            while True:

                if new_x < self.x_food:
                    new_x = self.x + random.randint(0,1)
                else:
                    new_x = self.x - random.randint(0,1)

                if new_y < self.y_food:
                    new_y = self.y + random.randint(0,1)
                else:
                    new_y = self.y - random.randint(0,1)

                ant_cords = (new_x, new_y)

                new_dist = math.dist(ant_cords, food_cords)

                if new_dist < 2:
                    self.x = self.x_food
                    self.y = self.y_food
                
                if new_dist < previous_dist:
                    break
                if new_dist == 0:
                    self.grab_food(self.x_food, self.y_food)
                    break

            self.x = new_x
            self.y = new_y

            # print(' x: ', self.x, ' y: ', self.y, ' dist: ',
            #       math.dist(ant_cords, food_cords))

            return 'alive'
        else:
            # Jeśli nie wyczuje jedzenia ide w losowym kierunku
            if random.randint(0,10) < 5:
                self.x += random.randint(0, self.speed)
            else:
                self.x -= random.randint(0, self.speed)

            if random.randint(0,10) < 5:
                self.y += random.randint(0, self.speed)
            else:
                self.y -= random.randint(0, self.speed)

            return 'alive'
            # print(' x: ', self.x, ' y: ', self.y, ' dist: ',
            #       math.dist(ant_cords, food_cords))

    def grab_food(self, x_food, y_food):
        taken_food = self.food.take_from(x_food, y_food)
        self.FoodAmmount = taken_food
        self.hasFood = True
        return 'alive'


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

        return 'alive'

        # print(' x: ', self.x, ' y: ', self.y, ' food: ', self.nest.food_stock)


# f = food_worker
# n = nest_worker
# ant = Ant(True, n, f)
# ant2 = Ant(False,n,f)

# food_worker.show()
# for i in range(500):
#     ant.Update()
#     ant2.Update()
# food_worker.show()
