from collections import Counter
import json
import random
from optparse import OptionParser

import networkx as nx
from PIL import Image, ImageDraw, ImageColor
from tqdm import tqdm
import utm


def load_graph(filename):
    json_data = json.load(open(filename, 'r'))
    G = nx.adjacency_graph(json_data)
    return G


def find_largest_strongly_connected_component(G):
    print("determining largest strongly connected component..")
    nodes_cc = max(tqdm(nx.kosaraju_strongly_connected_components(G)), key=len)
    Gcc = G.subgraph(nodes_cc)
    return Gcc


def find_approximate_central_node(G):
    print("finding approximate central node..")

    node_distances = Counter()
    start_nodes = random.sample(G.nodes, 20)

    for start_node_id in tqdm(start_nodes):
        lengths = Counter(nx.single_source_dijkstra_path_length(G, start_node_id))
        node_distances += lengths

    central_node = min(node_distances, key=node_distances.get)
    print("taking node with id {} as central node, with summed distance: {}".format(central_node, node_distances[central_node]))
    return central_node


def draw_graph_on_map(G, lengths, output_filename, width=1600, height=1200):
    print("preparing to draw graph...")
    # convert to simple lines
    lines = []
    max_x, max_y = float("-inf"), float("-inf")
    min_x, min_y = float("inf"), float("inf")
    max_distance = float("-inf")

    for e in tqdm(G.edges):
        s, t = e

        sx, sy, _, _ = utm.from_latlon(G.nodes[s]["lat"], G.nodes[s]["lon"])
        tx, ty, _, _ = utm.from_latlon(G.nodes[t]["lat"], G.nodes[t]["lon"])
        sy, ty = -sy, -ty  # need to invert y coordinates
        distance = max(lengths[s], lengths[t])
        if distance < float("inf"):
            max_distance = max(max_distance, distance)
        lines.append(((sx, sy), (tx, ty), distance))
        max_x, max_y = max(max_x, sx, tx), max(max_y, sy, ty)
        min_x, min_y = min(min_x, sx, tx), min(min_y, sy, ty)

    print("drawing...")
    picture_width = width
    picture_height = height
    denominator = max((max_x - min_x)/picture_width, (max_y - min_y)/picture_height)
    im = Image.new("RGB", (picture_width, picture_height), "#FFF")
    draw = ImageDraw.Draw(im)
    for line_data in tqdm(lines):
        # prepare coordinates to draw
        sx = (line_data[0][0] - min_x) / denominator
        tx = (line_data[1][0] - min_x) / denominator

        sy = (line_data[0][1] - min_y) / denominator
        ty = (line_data[1][1] - min_y) / denominator

        line = ((sx, sy), (tx, ty))

        # determine color
        distance = line_data[2]
        if distance < float("inf"):
            luminosity = float(distance) / float(max_distance) * 100.0
        else:
            luminosity = 100

        color = ImageColor.getrgb(f"hsl(233, 74%, {luminosity}%)")

        # draw line
        draw.line(line, fill=color)

    print("saving output file: {}".format(output_filename))
    im.save(output_filename, "PNG")


def travel_time(data):
    if not data["length"] or data["length"] == 0:
        return float("inf")
    return data["max_v"] / data["length"]


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="in_filename", action="store", type="string", help="input networkx JSON file")
    parser.add_option("-o", "--out", dest="out_filename", action="store", type="string", help="output png file")
    parser.add_option("-c", "--center", dest="center", action="store_true", help="set this option to compute the shortest distances from an approximate center node [default: random node]")
    parser.add_option("-m", "--metric", dest="metric", action="store", type="string", default="travel-time", help="metric for the shortest path algorithm. Either  'length' or 'travel-time' [default: travel-time]")
    parser.add_option("--width", dest="width", action="store", type="int", default=1600, help="image width in px [default=1600]")
    parser.add_option("--height", dest="height", action="store", type="int", default=1200, help="image height in px [default=1200]")
    (options, args) = parser.parse_args()

    if (options.in_filename is None) or (options.out_filename is None):
        parser.print_help()
        exit(-1)

    G = load_graph(options.in_filename)
    Gcc = find_largest_strongly_connected_component(G)
    if options.center:
        start_node = find_approximate_central_node(Gcc)
    else:
        start_node = random.choice(list(Gcc))

    metric = None
    if options.metric == "travel-time":
        metric = travel_time
    elif options.metric == "length":
        metric = "length"
    else:
        print("Did not recognize --metric/-m option. Provided {}. Must either be 'travel-time' or 'length'".format(options.metric))

    lengths = nx.single_source_dijkstra_path_length(Gcc, start_node, cutoff=None, weight=travel_time)
    draw_graph_on_map(Gcc, lengths, output_filename=options.out_filename)
