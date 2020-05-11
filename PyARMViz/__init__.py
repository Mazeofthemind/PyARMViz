#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Python Association Rule Visualization Library
"""

# We use semantic versioning
# See https://semver.org/
__version__ = "0.1.4"

import sys 

#Specific function
from PyARMViz.PyARMViz import adjacency_parallel_category_plot
from PyARMViz.PyARMViz import adjacency_parallel_coordinate_plot
from PyARMViz.PyARMViz import adjacency_graph_gephi
from PyARMViz.PyARMViz import adjacency_graph_plotly
from PyARMViz.PyARMViz import adjacency_scatter_plot
from PyARMViz.PyARMViz import metadata_scatter_plot