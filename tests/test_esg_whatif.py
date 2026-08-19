from src.core.esg_calculator import calculate_co2_grams, generate_esg_report

def test_co2_calculation_positive():
    assert calculate_co2_grams(10) > 0

def test_co2_scales_with_distance():
    assert calculate_co2_grams(20) > calculate_co2_grams(10)

def test_esg_report_structure(graph):
    import networkx as nx
    nodes= list(graph.nodes())
    start, end= nodes[0], nodes[5]
    if not nx.has_path(graph, start, end):
        return
    path= nx.shortest_path(graph, start, end, weight="distance")
    report= generate_esg_report(graph, path, path)
    assert report["co2_saved_pct"] == 0