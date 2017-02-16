import sh
import unittest
from subprocess import call
import os
import hashlib


class IntegrationTest(unittest.TestCase):

    ClassIsSetup = False

    def setUp(self):
        if not self.ClassIsSetup:
            self.bar()
            self.__class__.ClassIsSetup = True

    def bar(self):
        call(["python", "run.py", "-f", "data/karlsruhe_small.osm", "-n", "p", "-c"])

    def pedestrian_graph_ok_test(self):
        self.assertEquals(hashlib.md5(open("data/karlsruhe_small.pypgr", 'rb').read()).hexdigest(), "95353414f78a965fc8375e6df03c9910")

    def pedestrian_graph_names_ok_test(self):
        self.assertEquals(hashlib.md5(open("data/karlsruhe_small.pypgr_names", 'rb').read()).hexdigest(), "7bb07a5cb0d716332a787db0694201a9")

    @unittest.skip("testing skipping")
    def pedestrian_graph_c_names_ok_test(self):
        self.assertEquals(hashlib.md5(open("data/karlsruhe_small.pypgrc_names", 'rb').read()).hexdigest(), "3eec807f0b21c25a535b31a4f09a0881")

    @unittest.skip("testing skipping")
    def pedestrian_graph_c_ok_test(self):
        self.assertEquals(hashlib.md5(open("data/karlsruhe_small.pypgrc", 'rb').read()).hexdigest(), "bea4d974990b5e9f022e57903ae0baa5")
