import numpy as np
from evo import Evolution, TSP
import matplotlib.pyplot as plt
import random

def tsp_fitness_creator(cities):
    matrix = []
    for city in cities:
        row = []
        for city_ in cities:
            row.append(np.linalg.norm(city - city_))
        matrix.append(row)
    distances = np.array(matrix)

    def fitness(tsp):
        res = 0
        for i in range(len(tsp.value)):
            res += distances[tsp.value[i], tsp.value[(i + 1) % len(tsp.value)]]
        return -res

    return fitness


def compute_distances(cities):
    distances = []
    for from_city in cities:
        row = []
        for to_city in cities:
            row.append(np.linalg.norm(from_city - to_city))
        distances.append(row)
    return np.array(distances)


def route_length(distances, route):
    length = 0
    for i in range(len(route)):
        length += distances[route[i], route[(i + 1) % len(route)]]
    return length


def plot_route(cities, route, distances):
    length = route_length(distances, route)

    plt.figure(figsize=(12, 8))
    plt.scatter(x=cities[:, 0], y=cities[:, 1], s=1000, zorder=1)
    for i in range(len(cities)):
        plt.text(cities[i][0], cities[i][1], str(i), horizontalalignment='center', verticalalignment='center', size=16,
                 c='white')
    for i in range(len(route)):
        plt.plot([cities[route[i]][0], cities[route[(i + 1) % len(route)]][0]],
                 [cities[route[i]][1], cities[route[(i + 1) % len(route)]][1]], 'k', zorder=0)
    if len(route)>0:
        plt.title(f'Visiting {len(route)} cities in length {length:.2f}', size=16)
    else:
        plt.title(f'{len(cities)} cities', size=16)
    plt.show()


cities=[]
for i in range(30):
    a=random.randrange(0, 50)
    b=random.randrange(0, 50)
    temp=[a,b]
    cities.append(temp)
    temp=[]
cities=np.array(cities)
fitness = tsp_fitness_creator(cities)
distances = compute_distances(cities)

evo = Evolution(
    pool_size=100, fitness=fitness, individual_class=TSP, n_offsprings=30,
    pair_params={'alpha': 0.5},
    mutate_params={'rate': 1},
    init_params={'n_cities': 20}
)
n_epochs = 1000

hist = []

for i in range(n_epochs):
    hist.append(evo.pool.fitness(evo.pool.individuals[-1]) *(-1))
    evo.step()
    if(i%100==0):
        plot_route(cities, route=evo.pool.individuals[-1].value, distances=distances)
    

plt.plot(hist)
plt.show()

#plot_route(cities, route=evo.pool.individuals[-1].value, distances=distances)
