import unittest
from PyARMViz import PyARMViz
from PyARMViz import datasets

import os

import logging

class MyTest(unittest.TestCase):
    
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        #logging.basicConfig(level=logging.INFO)
        
        self.rules = datasets.load_shopping_rules()
        
    def test_plotly_rule_graph(self):
        graph = PyARMViz.generate_rule_graph_plotly(self.rules,)
        self.assertTrue(True)
        #generate_rule_strength_plot(rules)
    def test_graphml_rule_graph(self):
        test_file_path = './test.gexf'
        graph = PyARMViz.generate_rule_graph_graphml(self.rules, test_file_path)
        self.assertTrue(os.path.exists(test_file_path))
    def test_plotly_rule_strength_plot(self):
        PyARMViz.generate_rule_strength_plot(self.rules)
        self.assertTrue(True)
    def test_plotly_parallel_coordinate_plot(self):
        PyARMViz.generate_parallel_coordinate_plot(self.rules)
    def test_plotly_parallel_category_plot(self):
        PyARMViz.generate_parallel_category_plot(self.rules)