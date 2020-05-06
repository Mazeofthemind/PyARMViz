#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Python Association Rule Visualization Library
"""

# We use semantic versioning
# See https://semver.org/
__version__ = "0.1.0"

import sys 

#Specific function
from PyARMViz.PyARMViz import generate_parallel_category_plot
from PyARMViz.PyARMViz import generate_parallel_coordinate_plot
from PyARMViz.PyARMViz import generate_rule_graph_graphml
from PyARMViz.PyARMViz import generate_rule_graph_plotly
from PyARMViz.PyARMViz import generate_rule_start_end_plot
from PyARMViz.PyARMViz import generate_rule_strength_plot