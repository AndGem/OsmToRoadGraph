import sh
import unittest
from subprocess import call
import os
import hashlib


class IntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        call(["python", "run.py", "-f", "data/karlsruhe_small.osm", "-n", "p", "-c"])

    def pedestrian_graph_ok_test(self):
        self.assertEquals(hashlib.md5(open("data/karlsruhe_small.pypgr", 'rb').read()).hexdigest(), "d363bc83c99222ff9ddc9094e3f06664")

    def pedestrian_graph_names_ok_test(self):
        self.assertEquals(hashlib.md5(open("data/karlsruhe_small.pypgr_names", 'rb').read()).hexdigest(), "2837fe0e24267d24a7b2e2335bcad687")

    def pedestrian_graph_c_names_ok_test(self):
        self.assertEquals(hashlib.md5(open("data/karlsruhe_small.pypgrc_names", 'rb').read()).hexdigest(), "3eec807f0b21c25a535b31a4f09a0881")

    def pedestrian_graph_c_ok_test(self):
        self.assertEquals(hashlib.md5(open("data/karlsruhe_small.pypgrc", 'rb').read()).hexdigest(), "bea4d974990b5e9f022e57903ae0baa5")
