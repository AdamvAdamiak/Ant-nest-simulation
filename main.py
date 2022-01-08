from networkx.algorithms.bipartite.basic import color
from ant import Ant
from food import food
from nest import nest
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
FOOD_VAL = 5
NEST_FOOD = 5
ANT_AMMOUNT = 46

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

    # nx.draw(G,nx.get_node_attributes(G,'pos'),with_labels=True,node_size=3000,node_color=color_map)
    # plt.show()


def draw_nest():
    G.add_node('Nest', pos=(0, 0))
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
            G.add_node(name,pos=(ant.x,ant.y))
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

food_worker = food(FOOD_VAL)
nest_worker = nest(NEST_FOOD, ANT_AMMOUNT)

ants = []
leaving_ants = []
nest_ants = []


for i in range(int(0.6*ANT_AMMOUNT)):
    leaving_ants.append(Ant(True, nest_worker, food_worker))

for i in range(int(0.4*ANT_AMMOUNT)):
    nest_ants.append(Ant(False, nest_worker, food_worker))

ants = leaving_ants + nest_ants


for i in range(500):
    # print(nest_worker.food_stock,nest_worker.ant_ammount)
    for ant in ants:
        state = ant.Update()
        if nest_worker.food_stock < 0:
            nest_worker.food_stock = 0
    draw_result()


