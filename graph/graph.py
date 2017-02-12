import codecs


class Graph(object):

    def __init__(self):
        self.edges = []
        self.vertices = []
        self.outneighbors = []
        self.inneighbors = []

    def add_edge(self, edge):
        self.edges.append(edge)

        if edge.forward:
            self.outneighbors[edge.s].add(edge.t)
            self.inneighbors[edge.t].add(edge.s)

        if edge.backward:
            self.outneighbors[edge.t].add(edge.s)
            self.inneighbors[edge.s].add(edge.t)

    def add_node(self, vertex):
        self.vertices.append(vertex)
        self.outneighbors.append(set())
        self.inneighbors.append(set())

    def edge_description(self, edge_id):
        return "{}".format(self.edges[edge_id].description)

    def edge_name(self, edge_id):
        return "{}".format(self.edges[edge_id].name)

    def all_neighbors(self, node_id):
        return list(self.outneighbors[node_id].union(self.inneighbors[node_id]))

    def write_to_file(self, filename_base, filename_ext):
        filename = "{}.{}".format(filename_base, filename_ext)
        print("writing {}".format(filename))

        file_header = "# Road Graph File v.0.3"
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

        f.write("{}\n".format(len(self.vertices)))
        f.write("{}\n".format(len(self.edges)))

        # write node information
        for v in self.vertices:
            f.write("{}\n".format(v))

        # write edge information
        for e in self.edges:
            f.write("{}\n".format(e.description))
            f_names.write(e.name)
            f_names.write("\n")

        f.close()
        f_names.close()
