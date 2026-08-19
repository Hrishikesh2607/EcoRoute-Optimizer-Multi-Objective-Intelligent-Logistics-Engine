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


def graph_aware_crossover(ind1, ind2):
    common_nodes= set(ind1[1:-1]) & set(ind2[1:-1])

    if not common_nodes:
        return ind1, ind2
    
    splice_node= random.choice(list(common_nodes))

    idx1= ind1.index(splice_node)
    idx2= ind2.index(splice_node)

    child1= ind1[:idx1] + ind2[idx2:]
    child2= ind2[:idx2] + ind1[idx1:]

    def is_valid_path(path):
        return all(G.has_edge(u,v) for u,v in zip(path[:-1], path[1:]))
    
    if not is_valid_path(child1):
        child1= ind1
    if not is_valid_path(child2):
        child2= ind2

    return creator.Individual(child1), creator.Individual(child2)

toolbox.register("mate", graph_aware_crossover)

def evaluate(individual, weight_time=0.5, weight_cost= 0.5):
    total_duration=0
    total_fare=0
    for u,v in zip(individual[:-1], individual[1:]):
        if not G.has_edge(u,v):
            return (1e6,)
        total_duration += G[u][v]["duration"]
        total_fare += G[u][v]["fare"]

    normalized_duration= total_duration / 60.0
    normalized_fare= total_fare / 20.0

    weighted_score= (weight_time * normalized_duration) + (weight_cost * normalized_fare)
    return (weighted_score,)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox.register("select", tools.selTournament, tournsize=3)

def run_ga(start, end, weight_time=0.5, weight_cost=0.5, generations=50, pop_size=80):
    pop = [make_individual(start, end) for _ in range(pop_size)]
    best_per_gen = []

    for gen in range(generations):
        fitnesses = [evaluate(ind, weight_time, weight_cost) for ind in pop]
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        best = min(pop, key=lambda i: i.fitness.values[0])
        best_per_gen.append(best.fitness.values[0])

        pop = toolbox.select(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in pop]

        for i in range(0, len(offspring) - 1, 2):
            if random.random() < 0.6:  
                offspring[i], offspring[i+1] = toolbox.mate(offspring[i], offspring[i+1])

        for ind in offspring:
            if random.random() < 0.3:  
                toolbox.mutate(ind)
            del ind.fitness.values

        pop = offspring

    best = min(pop, key=lambda i: evaluate(i, weight_time, weight_cost)[0])
    print("Best path:", best)
    print("Best fitness:", evaluate(best, weight_time, weight_cost))
    print("Convergence trend (first 5, last 5):", best_per_gen[:5], best_per_gen[-5:])
    return best, best_per_gen

def evaluate_with_fuel_multiplier(individual, weight_time=0.5, weight_cost=0.5, fuel_multiplier=1.0):
    total_duration=0
    total_fare=0
    for u,v in zip(individual[:-1], individual[1:]):
        if not G.has_edge(u,v):
            return(1e6,)
        total_duration += G[u][v]["duration"]
        total_fare += G[u][v]["fare"]*fuel_multiplier

    normalized_duration=total_duration / 60.0
    normalized_fare= total_fare / 20.0
    weighted_score= (weight_time*normalized_duration) + (weight_cost * normalized_fare)
    return (weighted_score,)

def run_ga_scenario(start, end, weight_time=0.5, weight_cost=0.5,
                    fuel_multiplier=1.0, generations=50, pop_size=80):
    pop= [make_individual(start, end) for _ in range(pop_size)]

    for gen in range(generations):
        fitnesses= [evaluate_with_fuel_multiplier(ind, weight_time, weight_cost, fuel_multiplier) for ind in pop]
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.value= fit

        pop= toolbox.select(pop, len(pop))
        offspring= [toolbox.clone(ind) for ind in pop]

        for i in range(0, len(offspring) -1, 2):
            if random.random() < 0.6:
                offspring[i], offspring[i+1]= toolbox.mate(offspring[i], offspring[i+1])
        for ind in offspring:
            if random.random() < 0.3:
                toolbox.mutate(ind)
            del ind.fitness.values

        pop = offspring

    best= min(pop, key=lambda i: evaluate_with_fuel_multiplier(i, weight_time, weight_cost, fuel_multiplier)[0])
    return best

if __name__ == "__main__":
    start_node = list(G.nodes())[0]
    end_node = list(G.nodes())[10]
    run_ga(start_node, end_node)