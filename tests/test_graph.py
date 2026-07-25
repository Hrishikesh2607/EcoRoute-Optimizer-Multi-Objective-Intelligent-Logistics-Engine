def test_graph_has_nodes(graph):
    assert graph.number_of_nodes() > 0

def test_graph_has_edges(graph):
    assert graph.number_of_edges() > 0

def test_all_edges_have_required_weights(graph):
    for u,v, data in graph.edges(data=True):
        assert "duration" in data
        assert "fare" in data
        assert data["duration"] > 0
        assert data["fare"] > 0

def test_no_self_loop(graph):
    assert not any(u == v for u,v in graph.edges())

def test_graph_reasonable_node_count(graph):
    assert 50 <= graph.number_of_nodes() <= 300