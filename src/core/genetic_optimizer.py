import random
import networkx as nx
from deap import base, creator, tools
import pickle

G = pickle.load(open("data/processed/route_graph.gpickle", "rb"))

creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox= base.Toolbox()

def random_valid_path(start, end, max_hops=8):
    for _ in range(50):
        path= [start]
        current= start
        for _ in range(max_hops):
            if current == end:
                return path
            neighbors= list(G.successors(current))
            if not neighbors:
                break
            current= random.choice(neighbors)
            path.append(current)
        if path[-1] == end:
            return path
    return None

def make_individual(start, end):
    path= None
    while path is None:
        path= random_valid_path(start, end)
    return creator.Individual(path)

def evaluate(individual, weight_time=0.5, weight_cost=0.5):
    total_duration=0
    total_fare= 0
    for u,v in zip(individual[:-1], individual[1:]):
        if not G.has_edge(u,v):
            return(1e6, 1e6)
        total_duration += G[u][v]["duration"]
        total_duration += G[u][v]["fare"]
    return (total_duration, total_fare)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("select", tools.selNSGA2)

def custom_mutate(individual, indpb=0.2):
    for i in range(1, len(individual) - 1):  
        if random.random() < indpb:
            neighbors = list(G.successors(individual[i - 1]))
            if neighbors:
                individual[i] = random.choice(neighbors)
    return (individual,)

toolbox.register("mutate", custom_mutate)

def run_ga(start, end, generations=30, pop_size=50):
    pop = [make_individual(start, end) for _ in range(pop_size)]

    for gen in range(generations):
        fitnesses = [evaluate(ind) for ind in pop]
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        pop = toolbox.select(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in pop]

        for ind in offspring:
            toolbox.mutate(ind)
            del ind.fitness.values

        pop = offspring

    best = tools.selBest(pop, 1)[0]
    print("Best path:", best)
    print("Fitness (duration, fare):", best.fitness.values if best.fitness.valid else evaluate(best))
    return best

if __name__ == "__main__":
    start_node = list(G.nodes())[0]
    end_node = list(G.nodes())[10]
    run_ga(start_node, end_node)