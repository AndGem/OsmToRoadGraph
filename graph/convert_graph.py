try:
    import networkx as nx
except ImportError:
    pass


def convert_to_networkx(graph):
    out_graph = nx.DiGraph()

    for v in graph.vertices:
        data_dict = {s: getattr(v.data, s) for s in v.data.__slots__}
        out_graph.add_node(v.id, **data_dict)

    for e in graph.edges:
        data_dict = {s: getattr(e.data, s) for s in e.data.__slots__}
        out_graph.add_edge(e.s, e.t, **data_dict)
        if e.backward:
            out_graph.add_edge(e.t, e.s, **data_dict)

    return out_graph
