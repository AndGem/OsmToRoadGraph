import codecs
import json

try:
    import networkx as nx
except ImportError:
    pass


def write_to_file(graph, filename_base, filename_ext):
    filename = "{}.{}".format(filename_base, filename_ext)
    print("writing output file: {}".format(filename))

    file_header = "# Road Graph File v.0.4"
    header = """# number of nodes
# number of edges
# node_properties
# ...
# edge_properties
# ..."""

    f = open(filename, "w")
    f_names = codecs.open("{}_names".format(filename), "w", "utf-8")

    f.write("{}\n".format(file_header))
    f.write("{}\n".format(header))

    f.write("{}\n".format(len(graph.vertices)))
    f.write("{}\n".format(len(graph.edges)))

    # write node information
    for v in graph.vertices:
        f.write("{}\n".format(v.description))

    # write edge information
    for e in graph.edges:
        f.write("{}\n".format(e.description))
        f_names.write(e.data.name)
        f_names.write("\n")

    f.close()
    f_names.close()


def write_nx_to_file(nx_graph, filename):

    print("writing networkx output file: {}".format(filename))
    json_out = nx.adjacency_data(nx_graph)

    f = open(filename, "w")
    json.dump(json_out, f)
    f.close()
