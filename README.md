# Introduction

Advanced Python Association Rule Visualization Library

# Summary

Loosely based on [ARulesViz](https://cran.r-project.org/web/packages/arulesViz/index.html) for R
and the ideas described in this [paper](https://link.springer.com/article/10.1007/s11573-016-0822-8).

[Association Rules Mining (ARM)](https://en.wikipedia.org/wiki/Association_rule_learning) produces 
Association Rules (AR) from mined Item Sets in a DataBase (DB). 
Most ARM libraries represent these output rules textually using the **Antecedent (predictor)**, 
**Consequent (predicted)** and **Descriptive Metadata (Support, Confidence, Lift, etc.)**
This presents a problem since typical DBs can yield 100-1000s of rules, forcing us to either apply
filtration criterion or devise more efficient visualizations.

While filtration is the most common and effective approach, dedicated visualizations are also valuable,
especially in data exploration scenarios where the characteristics of interesting data not may not be
known in advance

# Generating Rules
PyARMViz is designed to run on Association Rules like the ones produced by [Efficient-Apriori](https://pypi.org/project/efficient-apriori/)

The library includes a set of synthetic retail transaction data for testing and demonstration
purposes.
This data includes both transactions sets (to be run through a compatible ARM workflow of your choice)
or a rules set which can be input directly into the library.

```
from PyARMViz import datasets
rules = datasets.load_shopping_rules()
```

#Visualizations

The visualizations in this library can be divided into two families based on the data they display
about the individual Association Rules

## Rule Metadata Visualizations

Rule Metadata visualizations focus entirely on the descriptive metadata of each rule and do not
consider the antecedents and consequents.

This makes this visualization less helpful for discovering interesting regions in the original
data, but enables distributional evaluation of rules to develop better filtration criterion.

These visualization also tend to be among the most scalable because they do not need to display
multiple entity types (rule v. antecedent/precedent) simultaneously.

### Confidence/Lift/Support Scatterplot

The three primary descriptive metadata for rules are **Confidence** (percentage of time the 
antecedent leads to the consequent versus the support of the antecedent), the **Support** 
(percentage of times the antecedent leads to the consequent versus the size of the database) 
and the **Lift** (percentage of times the antecedent leads to the consequent versus the 
support of the consequent)

All three of these are commonly used filtration criterion for ARs, and by graphing their 
distribution, this visualization can help spot outlier and visually show the distribution of rules
that would pass a given set of criterion.

These new criterion can then be applied against the existing rules (as shown below), or upstream in the
analysts ARM workflow

```
from PyARMViz import datasets
from PyARMViz import PyARMViz

rules = datasets.load_shopping_rules()
PyARMViz.metadata_scatter_plot(rules)
```

## Rule Entity Visualizations
These visualizations include the **Antecedent** and **Consequent** **Entities** of the
**Rule** (ex. Antecedent:Eggs,Flour -> Consequent:Milk) with some portion of its descriptive
metadata.

These visualizations are useful for identifying the rules which are adjacent through their
terminating entities, and potentially complex structures such as hubs or chains formed by those
adjacencies.
These complex structures, in turn, can indicate regions of interest within the data which can be
extracted and inspected more closely.

### Parallel Plots
[Parallel plots](https://en.wikipedia.org/wiki/Parallel_coordinates) are a popular choice for 
large scale visualization of sets which highlights common elements in those sets.

All parallel plots work by taking multiple ordered sets of fixed length, assigning an axis to
each "place" in the set (ex. first item, second item, etc.). Assigning each value found in that
place to a location on the axis, and drawing a line between the locations assigned to each value
for each set. 

We can input our Association Rules into this visualization by converting each rule into an 
ordered set by appending the consequents to the antecedents (ex. antecedent1, antacedent2, 
consequent1) and visualizing them.

A major disadvantage of these diagrams for this purpose is that ARs are not of a fixed length.
Currently the library overcomes this by breaking the rules down by length and creating a different
plot for each.
This was chosen because Plotly does not allow us to input, forcing us to use some awkward padding
techniques that compromise readability.

#### Parallel Cordinate Plot
Parallel coordinate plots are the more common, popular and supported version of parallel plots.


#### Parallel Category Plot
The less popular, less well documented and (arguably) more appropriate choice for this application 
is [Parallel Category plots](https://plotly.com/python/parallel-categories-diagram/), sometimes 
called ribbon or Alluvial plots.
These are essentially the same as Parallel Coordinate plots except for how they allocate space on
the axis for each value.

While coordinate plots allocate a specific point per axis for each value in order to accomodate a theoretically
infinite number of values, category plots will allocate a segment of the axis based on the number
of values.

Optimally this subdivision will be based on the total number of sets that contain that value, 
giving us a way to demonstrate the frequency of individual and combinatorial values in the 
database.

The downside of this diagram, at least in the Plotly implementation, is that it provides less 
opportunity for visual highlighting of the characteristics of the individual role (size, color,
brightness).

### Network Diagrams
This group of diagrams (my favorite) work by turning the rules into a directional network graph
using the [NetworkX]() libary.

This allows us to leverage one of several potential graph visualizations to show the adjacency 
(shared Antecedents or Consequents) of rules and more complex structures (chains, hubs) formed
by that adjacency.

#### Plotly Network Diagram

This version uses the Plotly network diagram visualization to visualize the directional network
graph.

It has the advantage of being self contained in the browser and requiring no additional
dependencies aside from the base Plotly.

It has the disadvantage of limited arrangement algorithm and visual highlighting options when 
compared to dedicated graph visualization software.

```
from PyARMViz import datasets
from PyARMViz import PyARMViz

rules = datasets.load_shopping_rules()
adjacency_graph_plotly(rules)
```

#### Gephi Network Diagram Export
Network diagrams provide one of the most flexible, scalable and powerful visualizations in this
category but can result in highly interconnected graphs that are difficult and computationally
expensive to visualize. 
One solution is to use a dedicated, open source graph visualization tool like [Gephi](https://gephi.org/),
which provides a rich set of arrangement and visual highlighting options unavailable in a purely
Javascript solution such as Plotly

THe downside is that we will need to export the directional network graph from NetworkX to some
form that Gephi can use, in this case the GEFX file format.
After the file is output by this function, simply install Gephi, open it and load the output file
on disc.

Note that if an explicit destination location and filename is not provided, the function defaults to 
"rule.gexf" in the current working directory of the Python script calling the function.

```
from PyARMViz import datasets
from PyARMViz import PyARMViz

rules = datasets.load_shopping_rules()
adjacency_graph_gephi(rules)
```

# Installation

## From Github
1. In CLI (with Git setup locally) clone to local directory 
`git clone https://github.com/Mazeofthemind/PyARMViz.git`
2. Navigate into the root directory of the cloned project
`cd PyARMViz`
3. Execute Python build and install (may require sudo or alternate Python/PIP psudonym)
`pip install .`

## From PyPi (Currently only Testing)
`pip install --index-url https://test.pypi.org/simple/ PyARMViz`

# Build

This project is currently built under [Poetry](https://python-poetry.org/) a newer Python build tool leverage virtual 
environments

```
git clone https://github.com/Mazeofthemind/PyARMViz.git
pip install poetry
cd PyARMViz
python -m poetry build
'''