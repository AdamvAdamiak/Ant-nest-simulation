from math import exp
from networkx.algorithms.bipartite.basic import color
from ant import Ant
from food import food
from nest import nest
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
FOOD_VAL = 3
NEST_FOOD = 25
ANT_AMMOUNT = 50

G = nx.Graph()
color_map = []
size = []


def draw_food_sources():

    data = food_worker.get_graph_data()

    x = data[0]
    y = data[1]
    stock = data[2]

    for i in range(FOOD_VAL):
        name = 'Food' + str(i) + '\n' + 'stock: ' + str(stock[i])
        G.add_node(name, pos=(x[i], y[i]))
        color_map.append('orange')
        size.append(3000)


def draw_nest():
    name = 'Nest' + '\n' + 'Stock: ' + str(round(nest_worker.food_stock,2))
    G.add_node(name, pos=(0, 0))
    color_map.append('blue')
    size.append(3000)


def draw_graph():
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True,
            node_size=size, node_color=color_map)
    plt.show()


def draw_ants(ants):
    for i in range(len(ants)):
        ant = ants[i]
        name = 'a' + str(i)
        if ant.isLeavingNest == True:
            G.add_node(name, pos=(ant.x, ant.y))
            if ant.isDead == True:
                color_map.append('red')
            else:
                color_map.append('green')
            size.append(200)


def draw_result():
    global G
    global color_map
    global size

    G = nx.Graph()
    color_map = []
    size = []
    draw_food_sources()
    draw_nest()
    draw_ants(ants)
    draw_graph()


def create_ants():
    ants = []
    leaving_ants = []
    nest_ants = []

    for i in range(int(0.6*ANT_AMMOUNT)):
        leaving_ants.append(Ant(True, nest_worker, food_worker))

    for i in range(int(0.4*ANT_AMMOUNT)):
        nest_ants.append(Ant(False, nest_worker, food_worker))

    ants = leaving_ants + nest_ants
    return ants


food_worker = food(FOOD_VAL)
nest_worker = nest(NEST_FOOD, ANT_AMMOUNT)
ants = create_ants()


# for i in range(1000):
#     # print(nest_worker.food_stock,nest_worker.ant_ammount)
#     previous_food_data = food_worker.get_graph_data()

#     for ant in ants:
#         try:
#             ant.Update()
#         except TypeError:
#             break
#         if nest_worker.food_stock < 0:
#             nest_worker.food_stock = 0

#     next_food_data = food_worker.get_graph_data()
    
# draw_result()

def update(frame):
    for ant in ants:
        try:
            ant.Update()
        except TypeError:
            break
        if nest_worker.food_stock < 0:
            nest_worker.food_stock = 0
    plt.cla()
    draw_result()

ani = FuncAnimation(plt.gcf(),update)

plt.show()