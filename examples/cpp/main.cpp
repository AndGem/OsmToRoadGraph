#include <boost/config.hpp>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <iomanip>

#include <boost/graph/graph_traits.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>
#include <boost/graph/adjacency_list.hpp>
 
#include "io/ReadRG.h"

struct SimpleNode {
    double lat, lon;

    SimpleNode() {}
    SimpleNode(double lat, double lon) : lat(lat), lon(lon) {}
};

typedef boost::property<boost::edge_weight_t, double> EdgeWeightProperty;
typedef boost::adjacency_list < boost::listS, boost::vecS, boost::directedS,
    SimpleNode, EdgeWeightProperty > Graph;
typedef boost::graph_traits < Graph >::vertex_descriptor vertex_descriptor;
typedef boost::graph_traits < Graph >::edge_descriptor edge_descriptor;

typedef boost::graph_traits<Graph>::vertex_iterator vertex_iter; 

Graph build_graph(const NodeEdges& nodeEdges) {
    Graph graph;

    std::vector<Graph::vertex_descriptor> nodes;
    for (const Node& n: nodeEdges.nodes) {
        Graph::vertex_descriptor vertex = boost::add_vertex(graph);
        graph[vertex].lat = n.lat;
        graph[vertex].lon = n.lon;
        nodes.push_back(vertex);
    }
 
    for (const Edge& e: nodeEdges.edges) {
        boost::add_edge(nodes[e.s], nodes[e.t], e.weight, graph);
    }

    return graph;
}

std::string line_string(double lat1, double lon1, double lat2, double lon2) {
    std::ostringstream out;
    out << std::setprecision(10);
    out << "<Placemark>";
    out << "<styleUrl>#linestyleExample</styleUrl>" << std::endl;
    out << "<LineString><coordinates>" << std::endl;
    out << lon1 << ", " << lat1 << ", 0." << std::endl;
    out << lon2 << ", " << lat2 << ", 0." << std::endl;
    out << "</coordinates></LineString></Placemark>";
    return out.str();
}

std::string point_marker(double lat, double lon) {
    std::ostringstream out;
    out << std::setprecision(10);
    out << "<Placemark><Point><coordinates>" << std::endl;
    out << lon << ", " << lat << ", 0." << std::endl;
    out << "</coordinates></Point></Placemark>" << std::endl;
    return out.str();
}

static string hexColor(int val = 255, int min = 0, int max = 255) {
    std::stringstream out;
    out << "<Style id=\"linestyleExample\"><LineStyle>" << std::endl;
    out << "<color>" << std::endl;
    out << "f0000ff" << std::endl;
    out << "</color>" << std::endl;
    out << "<width>1</width>" << std::endl;
    out << "</LineStyle></Style>" << std::endl;
    return out.str();
}


void to_kml(const Graph& graph, const vertex_descriptor& start, const std::vector<vertex_descriptor>& parents, std::vector<int>& distances) {
    const std::string filename = "out.kml";
    std::ofstream f(filename);
    const std::string header = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><kml xmlns=\"http://earth.google.com/kml/2.0\"><Document>";
    f << header << std::endl;

    f << point_marker(graph[start].lat, graph[start].lon);
    boost::graph_traits < Graph >::vertex_iterator vertexIterator, vend;
    for (boost::tie(vertexIterator, vend) = boost::vertices(graph); vertexIterator != vend; ++vertexIterator) {
        std::string middle = line_string(graph[*vertexIterator].lat, graph[*vertexIterator].lon, graph[parents[*vertexIterator]].lat, graph[parents[*vertexIterator]].lon);
        std::cout << middle << std::endl;
        f << middle << std::endl;
    }
    std::cout << std::endl;

    const std::string footer = "</Document> </kml>";
    f << footer << std::endl;
}

void dijkstra(Graph& graph, int id) {
    std::vector<vertex_descriptor> parents(boost::num_vertices(graph));
    std::vector<int> distances(boost::num_vertices(graph));    
    
    std::pair<vertex_iter, vertex_iter> vp = vertices(graph);
    vertex_descriptor start = *(vp.first);
    boost::dijkstra_shortest_paths(graph, start, boost::predecessor_map(&parents[0]).distance_map(&distances[0]));
    to_kml(graph, start, parents, distances);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "missing filename!" << std::endl;
        std::cout << "./dijkstra <filename>" << std::endl;
        return -1;
    }

    NodeEdges nodesAndEdges = ReadRG::read_graph("../../data/karlsruhe_small.pycgr");
    Graph graph = build_graph(nodesAndEdges);
    dijkstra(graph, 0);
 
  return 0;
}
