import codecs
import json

try:
    import networkx as nx
except ImportError:
    pass


def write_to_file(graph, filename_base, filename_ext):
    filename = f"{filename_base}.{filename_ext}"
    print(f"writing output file: {filename}")

    file_header = "# Road Graph File v.0.4"
    header = """# number of nodes
# number of edges
# node_properties
# ...
# edge_properties
# ..."""

    with open(filename, "w", encoding="utf-8") as f, codecs.open(
        f"{filename}_names", "w", "utf-8"
    ) as f_names:
        f.write(f"{file_header}\n")
        f.write(f"{header}\n")

        f.write(f"{len(graph.vertices)}\n")
        f.write(f"{len(graph.edges)}\n")

        # write node information
        for v in graph.vertices:
            f.write(f"{v.description}\n")

        # write edge information
        for e in graph.edges:
            f.write(f"{e.description}\n")
            f_names.write(e.data.name)
            f_names.write("\n")

    f.close()
    f_names.close()


def write_nx_to_file(nx_graph, filename):
    print(f"writing networkx output file: {filename}")
    json_out = nx.adjacency_data(nx_graph)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_out, f)
