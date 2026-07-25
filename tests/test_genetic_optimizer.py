import networkx as nx
from src.core.genetic_optimizer import run_ga, evaluate, random_valid_path

def get_test_pair(graph):
    for node in list(graph.nodes())[:50]:
        for target in list(graph.nodes())[:50]:
            if node != target and nx.has_path(graph, node, target):
                return node, target
    raise ValueError("No reachable pair found in first 50 nodes - widen search")

def test_random_valid_path_produce_connected_path(graph):
    start, end= get_test_pair(graph)
    path= random_valid_path(start, end)
    assert path is not None
    assert path[0] == start
    assert path[1] == end
    for u,v in zip(path[:-1], path[1:]):
        assert graph.has_edge(u,v)

def test_ga_fitness_improves_or_holds_over_generations(graph):
    start,end = get_test_pair(graph)
    _, convergence= run_ga(start, end, generations=15, pop_size=30)
    for i in range(1, len(convergence)):
        assert convergence[i] <= convergence[i-1] + 1e-6

def test_invalid_path_is_heavily_penalized():
    fake_individual= [999999, 999998]
    score= evaluate(fake_individual)
    assert score[0] >= 1e6