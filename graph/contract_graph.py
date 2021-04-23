from collections import deque, defaultdict
from dataclasses import replace
from typing import DefaultDict, List, Set, Tuple

import graph.graphfactory as graphfactory
import utils.timer as timer

from graph.graph import Graph
from graph.graph_types import Vertex, Edge


class ContractGraph:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    @timer.timer
    def contract(self):
        self.out_edges_per_node = self._get_out_edges()
        all_new_edges = self._find_new_edges()
        node_ids = self._gather_node_ids(all_new_edges)
        nodes = self._get_nodes(node_ids)

        print(
            f"finished contracting: {len(all_new_edges)}/{len(self.graph.edges)} edges and {len(nodes)}/{len(self.graph.vertices)} vertices."
        )

        return graphfactory.build_graph_from_vertices_edges(nodes, all_new_edges)

    def _find_new_edges(self) -> Set[Edge]:
        #  maintain a list L of nodes from which we want to start searches to find new contracted edges
        #  initialize L with all intersection nodes (i.e., all nodes with degree != 2)
        #   for each node n in L
        #     for each of n's neighbor
        #       search until:
        #           - an intersection node is found or edge is found
        #           - the next edge is different in it's structure (e.g., different highway type, different max speed, ...)
        self.start_nodes = self._find_all_intersections()
        self.seen_start_nodes = set(self.start_nodes)
        new_edges = set()
        bidirectional_edges: Set[Tuple[int, int]] = set()

        out_edges_per_node = self._get_out_edges()
        while len(self.start_nodes) > 0:
            node_id = self.start_nodes.popleft()

            out_edges = out_edges_per_node[node_id]
            for first_out_edge in out_edges:
                start_node_id = node_id

                edges_to_merge, final_node_id = self._find_edges_to_merge(
                    start_node_id, first_out_edge
                )

                if len(edges_to_merge) == 0:
                    continue

                sum_edge_lengths = sum([e.data.length for e in edges_to_merge])
                data = replace(edges_to_merge[0].data, length=sum_edge_lengths)

                if edges_to_merge[0].backward:
                    #  deduplication measure; if not for this for bidirectional edges, that are
                    #  removed between intersections, 2 new edges would be created
                    smaller_node_id = (
                        start_node_id
                        if start_node_id < final_node_id
                        else final_node_id
                    )
                    bigger_node_id = (
                        start_node_id
                        if start_node_id > final_node_id
                        else final_node_id
                    )
                    if (smaller_node_id, bigger_node_id) in bidirectional_edges:
                        # already added this edge skip it
                        continue
                    bidirectional_edges.add((smaller_node_id, bigger_node_id))
                    merged_edge = Edge(
                        smaller_node_id,
                        bigger_node_id,
                        True,
                        edges_to_merge[0].backward,
                        data,
                    )
                else:
                    merged_edge = Edge(
                        start_node_id,
                        final_node_id,
                        True,
                        edges_to_merge[0].backward,
                        data,
                    )
                new_edges.add(merged_edge)
        return new_edges

    def _find_edges_to_merge(
        self, start_node_id: int, first_out_edge: Edge
    ) -> Tuple[List[Edge], int]:
        # walk from start_node along first_out_edge until:
        #  i) another intersection node is found
        #  ii) an edge is encountered on the way that is different (different name, max_speed, ...)
        #  iii) the start_node is found => loop [remove it completely]
        used_edges = []
        out_edge = first_out_edge
        current_node_id = start_node_id
        while True:
            used_edges.append(out_edge)
            next_node_id = out_edge.t if out_edge.s == current_node_id else out_edge.s

            if next_node_id == start_node_id:
                # detected a loop => remove it
                used_edges = []
                break

            if self._is_intersection(next_node_id):
                break

            next_out_edges = list(
                filter(
                    lambda e: current_node_id not in (e.s, e.t),
                    self.out_edges_per_node[next_node_id],
                )
            )

            if len(next_out_edges) == 0:
                # detected a dead end => stop
                break

            if len(next_out_edges) > 1:
                # something is wrong.. this should have been filtered out by the intersection check
                assert False

            next_out_edge = next_out_edges[0]
            if self._is_not_same_edge(out_edge, next_out_edge):
                if next_node_id not in self.seen_start_nodes:
                    # found a new possible start node
                    self.seen_start_nodes.add(next_node_id)
                    self.start_nodes.append(next_node_id)
                # break since we need to stop here
                break

            out_edge = next_out_edge
            current_node_id = next_node_id

        final_node_id = next_node_id
        return used_edges, final_node_id

    def _is_not_same_edge(self, e1: Edge, e2: Edge) -> bool:
        return (
            e1.data.highway != e2.data.highway
            or e1.data.max_v != e2.data.max_v
            or e1.data.name != e2.data.name
            or e1.backward != e2.backward
        )

    def _get_out_edges(self) -> DefaultDict[int, List[Edge]]:
        result: DefaultDict[int, List[Edge]] = defaultdict(list)
        for e in self.graph.edges:
            if e.forward:
                result[e.s].append(e)
            if e.backward:
                result[e.t].append(e)
        return result

    def _find_all_intersections(self) -> deque:
        node_ids = range(0, len(self.graph.vertices))
        return deque(filter(self._is_intersection, node_ids))

    def _get_nodes(self, node_ids: Set[int]) -> List[Vertex]:
        return list(map(self.graph.get_node, node_ids))

    def _gather_node_ids(self, edges: List[Edge]) -> Set[int]:
        print("\t gathering nodes...")
        node_ids = set()
        for e in edges:
            node_ids.add(e.s)
            node_ids.add(e.t)
        return node_ids

    def _is_intersection(self, node_id: int) -> bool:
        return len(self.graph.all_neighbors(node_id)) != 2
