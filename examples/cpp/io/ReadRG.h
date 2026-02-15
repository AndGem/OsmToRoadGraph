#include <fstream>
#include <iostream>
#include <string>
#include <vector>


struct Node {
    double lat, lon;

    Node() {};
    Node(double lat, double lon) : lat(lat), lon(lon) {}
};

struct Edge {
    int s, t;
    double weight;

    Edge() {};
    Edge(int s, int t, double weight) : s(s), t(t), weight(weight) {}
};

struct NodeEdges {
    std::vector<Node> nodes;
    std::vector<Edge> edges;
};

class ReadRG {
public:
    static NodeEdges read_graph(std::string filename) {
        std::fstream f(filename);

        if (!f.is_open()) {
            std::cout << "failed to open " << filename << std::endl;
            return NodeEdges();
        }

        std::cout << "opened " << filename << std::endl;
        if (!header_valid(f)) {
            return NodeEdges();
        }
        skip_commented_lines(f);

        int nmb_nodes{-1};
        int nmb_edges{-1};
        f >> nmb_nodes >> nmb_edges;

        std::cout << "graph contains: " << nmb_nodes << " nodes and " << nmb_edges << " edges" << std::endl;

        NodeEdges result;
        result.nodes = read_nodes(f, nmb_nodes);
        result.edges = read_edges(f, nmb_edges);
        return result;
    }

private:
    static bool header_valid(std::fstream& f) {
        const std::string expected_header = "# Road Graph File v.0.3";
        std::string header;
        std::getline(f, header);
        if (header != expected_header) {
            std::cout << "header mismatch! expected: " << expected_header << " read: " << header << std::endl;
            return false;
        }
        std::cout << "header check passed!" << std::endl;
        return true;
    }

    static void skip_commented_lines(std::fstream& f) {
        std::string dummy;
        while(f.peek() == '#') {
            std::getline(f, dummy);
        }
    }

    static std::vector<Node> read_nodes(std::fstream& f, const int nmb_nodes) {
        std::cout << "reading nodes... " << std::flush;
        std::vector<Node> nodes;
        for (int i = 0; i < nmb_nodes; ++i) {
            assert(!f.eof());
            print_progress(i, nmb_nodes);
            double x, y;
            int index;
            f >> index >> x >> y;
            nodes.emplace_back(x, y);
        }
        std::cout << " done!" << std::endl;
        return nodes;
    }

    static std::vector<Edge> read_edges(std::fstream& f, const int nmb_edges) {
        std::cout << "reading edges... " << std::flush;
        std::vector<Edge> edges;
        for (int i = 0; i < nmb_edges; ++i) {
            assert(!f.eof());
            print_progress(i, nmb_edges);

            int s, t;
            double length;
            std::string category;
            int speed;
            std::string forward, backward;

            f >> s >> t >> length >> category >> speed >> forward >> backward;

            const double time = (1.0/((double)speed * 1000.0 / 3600.0) * 100.0 * (double)length);
            if (forward == "True") {
                edges.emplace_back(s, t, time);
            } 
            if (backward == "True") {
                edges.emplace_back(t, s, time);
            }
        }
        std::cout << " done!" << std::endl;
        return edges;
    }

    static inline void print_progress(int i, int max) {
        if (i == (int)(max * 0.25)) {
            std::cout << "..25%" << std::flush;
        } else if (i == (int)(max * 0.5)) {
            std::cout << "\t ..50%" << std::flush;
        } else if (i == (int)(max * 0.75)) {
            std::cout << "\t ..75%" << std::flush;
        } else if (i == (int)(max - 1)) {
            std::cout << "\t ..100%" << std::flush;
        }
    }

};
