from dataclasses import dataclass
from enum import Enum
from optparse import OptionParser
import sys

from PIL import Image, ImageDraw, ImageColor
import utm


@dataclass
class Node:
    lat: float
    lon: float


@dataclass
class Edge:
    source_id: int
    target_id: int
    max_speed: int


class InputState(Enum):
    NMB_NODES = 2
    NMB_EDGES = 3
    NODES = 4
    EDGES = 5


def draw_graph(nodes, edges, width, height, text, out_filename):
    print("creating edges...")
    # convert to simple lines
    lines = []
    max_x, max_y = float("-inf"), float("-inf")
    min_x, min_y = float("inf"), float("inf")

    for e in edges:
        if (e.source_id not in nodes) or (e.target_id not in nodes):
            print(f"didn't find {e.source_id} or {e.target_id}")
            continue

        s, t = nodes[e.source_id], nodes[e.target_id]
        sx, sy, _, _ = utm.from_latlon(s.lat, s.lon)
        tx, ty, _, _ = utm.from_latlon(t.lat, t.lon)
        sy, ty = -sy, -ty  # need to invert y coordinates
        lines.append(((sx, sy), (tx, ty), e.max_speed))
        max_x, max_y = max(max_x, sx, tx), max(max_y, sy, ty)
        min_x, min_y = min(min_x, sx, tx), min(min_y, sy, ty)

    print("drawing...")
    picture_width = width
    picture_height = height
    denominator = max((max_x - min_x) / picture_width, (max_y - min_y) / picture_height)
    im = Image.new("RGB", (picture_width, picture_height), "#FFF")
    draw = ImageDraw.Draw(im)
    for line_data in lines:
        # prepare coordinates to draw
        sx = (line_data[0][0] - min_x) / denominator
        tx = (line_data[1][0] - min_x) / denominator

        sy = (line_data[0][1] - min_y) / denominator
        ty = (line_data[1][1] - min_y) / denominator

        line = ((sx, sy), (tx, ty))

        # determine color
        max_speed = line_data[2]
        luminosity = max(-8.0 / 5.0 * max_speed + 70.0, 0)
        color = ImageColor.getrgb(f"hsl(233, 74%, {luminosity}%)")

        # draw line
        draw.line(line, fill=color)

    draw.text((10, picture_height - 50), text, fill="#FF0000")
    draw.text(
        (10, picture_height - 30),
        "Map data © OpenStreetMap contributors",
        fill="#FF0000",
    )
    del draw

    im.save(out_filename, "PNG")


def read_file(filename):
    print(f"reading file {filename}...")
    state = InputState.NMB_NODES

    nodes = {}
    edges = []
    nmb_nodes = None
    nmb_edges = None
    with open(filename, "r", encoding="utf-8") as input_file:
        for line in input_file:
            if line.startswith("#"):
                continue

            if state == InputState.NMB_NODES:
                nmb_nodes = int(line)
                state = InputState.NMB_EDGES
            elif state == InputState.NMB_EDGES:
                nmb_edges = int(line)
                state = InputState.NODES
            elif state == InputState.NODES:
                node_id, lat, lon = line.split(" ")
                nodes[int(node_id)] = Node(float(lat), float(lon))
                if len(nodes) == nmb_nodes:
                    state = InputState.EDGES
            elif state == InputState.EDGES:
                (
                    source_id,
                    target_id,
                    _,
                    street_type,
                    max_speed,
                    bidirectional,
                ) = line.split(" ")
                edges.append(Edge(int(source_id), int(target_id), int(max_speed)))

    print(f"#nodes:{nmb_nodes}, #edges:{nmb_edges}")
    return nodes, edges


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="in_filename", action="store", type="string")
    parser.add_option("-o", "--out", dest="out_filename", action="store", type="string")
    parser.add_option(
        "-t",
        "--text",
        dest="text",
        action="store",
        type="string",
        default="",
        help="text drawn in lower left corner",
    )
    parser.add_option(
        "--width",
        dest="width",
        action="store",
        type="int",
        default=1600,
        help="image width in px [default=1600]",
    )
    parser.add_option(
        "--height",
        dest="height",
        action="store",
        type="int",
        default=1200,
        help="image height in px [default=1200]",
    )
    (options, args) = parser.parse_args()

    if (options.in_filename is None) or (options.out_filename is None):
        parser.print_help()
        sys.exit()

    nodes, edges = read_file(options.in_filename)
    draw_graph(
        nodes, edges, options.width, options.height, options.text, options.out_filename
    )
