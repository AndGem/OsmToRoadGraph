#include <boost/config.hpp>
#include <iostream>
#include <fstream>
 
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>
#include <boost/graph/adjacency_list.hpp>
 
#include "io/ReadRG.h"

typedef boost::property<boost::edge_weight_t, double> EdgeWeightProperty;
typedef boost::adjacency_list < boost::listS, boost::vecS, boost::directedS,
    boost::no_property, EdgeWeightProperty > Graph;
typedef boost::graph_traits < Graph >::vertex_descriptor vertex_descriptor;
typedef boost::graph_traits < Graph >::edge_descriptor edge_descriptor;

typedef boost::graph_traits<Graph>::vertex_iterator vertex_iter; 

Graph build_graph(const NodeEdges& nodeEdges) {
    Graph graph;

    std::vector<Graph::vertex_descriptor> nodes;
    for (const Node& n: nodeEdges.nodes) {
        Graph::vertex_descriptor vertex = boost::add_vertex(graph);
        nodes.push_back(vertex);
    }
 
    for (const Edge& e: nodeEdges.edges) {
        boost::add_edge(nodes[e.s], nodes[e.t], e.weight, graph);
    }

    return graph;
}

void dijkstra(Graph& graph, int id) {
    std::vector<vertex_descriptor> parents(boost::num_vertices(graph));
    std::vector<int> distances(boost::num_vertices(graph));    
    
    std::pair<vertex_iter, vertex_iter> vp = vertices(graph);
    boost::dijkstra_shortest_paths(graph, *(++vp.first), boost::predecessor_map(&parents[0]).distance_map(&distances[0]));
    
    boost::graph_traits < Graph >::vertex_iterator vertexIterator, vend;
    for (boost::tie(vertexIterator, vend) = boost::vertices(graph); vertexIterator != vend; ++vertexIterator) {
        std::cout << "distance(" << *vertexIterator << ") = " << distances[*vertexIterator] << ", ";
        std::cout << "parent(" << *vertexIterator << ") = " << parents[*vertexIterator] << std::endl;
    }
    std::cout << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "missing filename!" << std::endl;
        std::cout << "./dijkstra <filename>" << std::endl;
        return -1;
    }

    NodeEdges nodesAndEdges = ReadRG::read_graph("../../data/karlsruhe_small.pypgr");
    Graph graph = build_graph(nodesAndEdges);
    dijkstra(graph, 0);
 
  return 0;
}
