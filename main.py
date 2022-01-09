from itertools import count
from math import exp
from networkx.algorithms.bipartite.basic import color
from ant import Ant
from food import food
from nest import nest
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
FOOD_VAL = 20
NEST_FOOD = 10
ANT_AMMOUNT = 50

G = nx.Graph()
color_map = []
size = []
labels = {}


def draw_food_sources():

    data = food_worker.get_graph_data()

    x = data[0]
    y = data[1]
    stock = data[2]

    for i in range(FOOD_VAL):
        name = 'Food' + str(i)
        G.add_node(name, pos=(x[i], y[i]))
        color_map.append('orange')
        size.append(1000)
        labels[name] = 'stock: ' + str(stock[i])


def draw_nest():
    name = 'Nest'
    G.add_node(name, pos=(0, 0))
    color_map.append('blue')
    size.append(3000)
    labels[name] = 'Stock: ' + str(round(nest_worker.food_stock, 2))


def draw_graph():
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True,
            node_size=size, node_color=color_map, labels=labels)
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


def draw_result(previous_data, next_data):
    global G
    global color_map
    global size
    global labels
    G = nx.Graph()
    color_map = []
    size = []
    labels = {}
    draw_food_sources()
    draw_nest()
    draw_ants(ants)
    for k in range(FOOD_VAL):
        if previous_data[2][k] != next_data[2][k]:
            G.add_edge('Nest', f'Food{k}')
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


def count_ants(l, val):
    r = 0
    for v in l:
        if v == val:
            r += 1
    return r


food_worker = food(FOOD_VAL)
nest_worker = nest(NEST_FOOD, ANT_AMMOUNT)
ants = create_ants()


leaving_ants = []
nest_ants = []
previous_food_data = food_worker.get_graph_data()
for i in range(501):
    stats = []
    for ant in ants:
        state = ant.Update()
        stats.append(state)
        if nest_worker.food_stock < 0:
            nest_worker.food_stock = 0
    print('Iteracja: ', i+1, ' Populacja: ', stats.count('alive'), ' Ilość jedzenia: ',round(nest_worker.food_stock,2))
    next_food_data = food_worker.get_graph_data()

    if i % 100 == 0:
        draw_result(previous_food_data, next_food_data)
        for i in range(int(0.2*ANT_AMMOUNT)):
            leaving_ants.append(Ant(True, nest_worker, food_worker))

        for i in range(int(0.1*ANT_AMMOUNT)):
            nest_ants.append(Ant(False, nest_worker, food_worker))

        ants += leaving_ants + nest_ants
        
        print(f'Urodziło się {len(leaving_ants) + len(nest_ants)} mrówek')

        leaving_ants = []
        nest_ants = []


# previous_food_data = food_worker.get_graph_data()
# def update(i):
#     stats = []
#     for ant in ants:
#         state = ant.Update()
#         stats.append(state)
#         if nest_worker.food_stock < 0:
#             nest_worker.food_stock = 0
#     print('Iteracja: ', i+1, ' Populacja: ', stats.count('alive'))
#     next_food_data = food_worker.get_graph_data()

#     plt.cla()
#     draw_result(previous_food_data, next_food_data)


# ani = FuncAnimation(plt.gcf(), update)

# plt.show()
