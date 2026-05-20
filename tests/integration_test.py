import importlib.util
import unittest
from subprocess import call

networkx_available = importlib.util.find_spec("networkx") is not None


class IntegrationTest(unittest.TestCase):
    def test_python(self):
        self._execute_program()
        self.pedestrian_graph_ok()
        self.pedestrian_graph_contracted_ok()

    def pedestrian_graph_ok(self):
        nmb_nodes, nmb_edges = self._get_nmb_nodes_edges("data/karlsruhe_small.pypgr")

        self.assertEqual(nmb_nodes, 4108)
        self.assertEqual(nmb_edges, 4688)

    def pedestrian_graph_contracted_ok(self):
        nmb_nodes, nmb_edges = self._get_nmb_nodes_edges("data/karlsruhe_small.pypgrc")

        self.assertEqual(nmb_nodes, 1469)
        self.assertEqual(nmb_edges, 2039)

    def _execute_program(self):
        args = ["python3", "run.py", "-f", "data/karlsruhe_small.osm", "-n", "p", "-c"]
        # --networkx requires the optional networkx dependency; only exercise
        # it when networkx is actually installed
        if networkx_available:
            args.append("--networkx")
        returncode = call(args)
        self.assertEqual(0, returncode)

    def _get_nmb_nodes_edges(self, path):
        with open(path) as f:
            line = f.readline()
            while "#" in line:
                line = f.readline()

            nmb_nodes = int(line)
            line = f.readline()
            nmb_edges = int(line)
            return nmb_nodes, nmb_edges
