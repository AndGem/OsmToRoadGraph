import codecs
import utils.timer as timer


def write_to_file(graph, filename_base, filename_ext):
    filename = "{}.{}".format(filename_base, filename_ext)
    print("writing {}".format(filename))

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
        f_names.write(e.name)
        f_names.write("\n")

    f.close()
    f_names.close()
