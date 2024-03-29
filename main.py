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
import random 
FOOD_VAL = 200
NEST_FOOD = 25
ANT_AMMOUNT = 250

G = nx.Graph()
color_map = []
size = []
labels = {}
edge_labels = {}
edge_colors = []
nest_data = [
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest1'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest2'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest3'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest4'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest5'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest6'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest7'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest8'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest9'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest10'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest11'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest12'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest13'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest14'],
    [random.randint(-120,120), random.randint(-120,120), NEST_FOOD, ANT_AMMOUNT, 'Nest15']]  # x y food ants


def draw_food_sources(food_worker,draw_a):
    global color_map
    global labels

    data = food_worker.get_graph_data()

    x = data[0]
    y = data[1]
    stock = data[2]
    visits = data[3]
    if draw_a == 0:
        color_map = []
        labels = {}
    for i in range(FOOD_VAL):
        name = 'Food' + str(i)

        if draw_a == 0 and visits[i] == 0:
            try:
                G.remove_node(name)
            except nx.exception.NetworkXError:
                pass
            continue
        G.add_node(name, pos=(x[i], y[i]))
        if stock[i] == 0:
            color_map.append('gray')
        else:
            color_map.append('orange')
        size.append(150)
        labels[name] = name + '\n' + 'stock: ' + str(stock[i])


    return visits


def draw_nest(nest_workers, nest_x, nest_y):
    for nest_worker in nest_workers:
        name = nest_worker.name
        G.add_node(name, pos=(nest_worker.x, nest_worker.y))
        color_map.append('blue')
        size.append(250)
        labels[name] = name + '\n' + 'Stock: ' + \
            str(round(nest_worker.food_stock, 2))


def draw_graph(draw_a):
    if draw_a == 1:
        pos = nx.get_node_attributes(G, 'pos')
        plt.xlim([-200, 200])
        plt.ylim([-200, 200])
    else:
        pos = nx.kamada_kawai_layout(G,scale=5)
        pos2 = nx.get_node_attributes(G, 'pos')
        edge_colors = nx.get_edge_attributes(G,'color').values()
        nx.draw(G, pos2, with_labels=True,node_size=size, node_color=color_map, labels=labels, edge_color=edge_colors)
        plt.show()
    # nx.draw_networkx_edge_labels(
    #     G, pos, edge_labels=edge_labels)
    edge_colors = nx.get_edge_attributes(G,'color').values()
    nx.draw(G, pos, with_labels=True,node_size=size, node_color=color_map, labels=labels, edge_color=edge_colors)

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
            size.append(5)


def draw_result(previous_data, next_data, ants, nest_workers, food_worker, nest_x, nest_y, draw_a=1):
    global G
    global color_map
    global size
    global labels
    global edge_labels
    global edge_colors
    G = nx.Graph()
    edge_labels = {}
    color_map = []
    size = []
    labels = {}
    visits = draw_food_sources(food_worker,draw_a)
    draw_nest(nest_workers, nest_x, nest_y)
    if draw_a == 1:
        draw_ants(ants)
    # for k in range(FOOD_VAL):
    #     if previous_data[2][k] != next_data[2][k]:
    #         for data in nest_data:
    #             name = data[4]
    #             G.add_edge(name, f'Food{k}')
    #             # edge_labels[(name, f'Food{k}')] = visits[k]

    for food_obj, i in zip(food_worker.food_places, range(len(food_worker.food_places))):
        for nest in food_obj.nest_visitors:
            G.add_edge(nest, f'Food{i}',color='orange')

    # for data in nest_data:
    #     name1 = data[4]
    #     for data2 in nest_data:
    #         name2 = data2[4]
    #         G.add_edge(name1, name2)
    for food_obj in food_worker.food_places:
        visitors = []
        for visitor in food_obj.nest_visitors:
            visitors.append(visitor)
        for v1 in visitors:
            for v2 in visitors:
                G.add_edge(v1,v2,color='blue')

    draw_graph(draw_a)


def create_ants(nest_workers, food_worker):
    ants = []
    leaving_ants = []
    nest_ants = []
    for nest_worker in nest_workers:
        nest_x = nest_worker.x
        nest_y = nest_worker.y
        for i in range(int(0.8*ANT_AMMOUNT)):
            leaving_ants.append(
                Ant(nest_x, nest_y, True, nest_worker, food_worker))

        for i in range(int(0.2*ANT_AMMOUNT)):
            nest_ants.append(
                Ant(nest_x, nest_y, False, nest_worker, food_worker))

    ants = leaving_ants + nest_ants
    return ants


def start(nests_info):
    global leaving_ants
    global nest_ants
    global previous_food_data

    food_worker = food(FOOD_VAL)
    nest_workers = []
    for data in nests_info:
        nest_x = data[0]
        nest_y = data[1]
        food_val = data[2]
        ant_ammount = data[3]
        name = data[4]
        nest_workers.append(nest(name, nest_x, nest_y, food_val, ant_ammount))
    ants = create_ants(nest_workers, food_worker)

    leaving_ants = []
    nest_ants = []
    previous_food_data = food_worker.get_graph_data()

    step = 500

    for i in range(1, 25000):
        stats = []
        for ant in ants:
            state = ant.Update()
            stats.append(state)
            if ant.nest.food_stock < 0:
                ant.nest.food_stock = 0

        nests_food = 0
        for nest_obj in nest_workers:
            nests_food += nest_obj.food_stock
        print('Iteracja: ', i, ' Populacja: ',
              stats.count('alive'), ' Ilość jedzenia: ', round(nests_food, 2))
        next_food_data = food_worker.get_graph_data()

        if stats.count('alive') == 0:
            print('Kolonia wymarła')
            break

        if i == 1:
            draw_result(previous_food_data, next_food_data, ants, nest_workers, food_worker, nest_x, nest_y)
        if i % step == 0:
            for nest_worker in nest_workers:
                for i in range(int(random.random()/10*ANT_AMMOUNT)):
                    leaving_ants.append(Ant(nest_worker.x,nest_worker.y,True, nest_worker, food_worker))

                for i in range(int(random.random()/10*ANT_AMMOUNT)):
                    nest_ants.append(Ant(nest_worker.x,nest_worker.y,False, nest_worker, food_worker))

            ants += leaving_ants + nest_ants
            
            print(f'Urodziło się {len(leaving_ants) + len(nest_ants)} mrówek')
            leaving_ants = []
            nest_ants = []

            print('Czy kontynuować symulacje [T/N]: ',end='')
            odp = str(input())
            
            draw_result(previous_food_data, next_food_data, ants,
                        nest_workers, food_worker, nest_x, nest_y)

            if odp == 'N':
                break

    draw_result(previous_food_data, next_food_data, ants,
                nest_workers, food_worker, nest_x, nest_y, 0)


start(nest_data[0:5])
start(nest_data[0:10])
start(nest_data[0:15])


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
