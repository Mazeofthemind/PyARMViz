# Introduction

Advanced Python Association Rule Visualization Library

# Summary

PyARMViz is based loosely on the [ARulesViz](https://cran.r-project.org/web/packages/arulesViz/index.html) package for R
and the ideas described in this [paper](https://link.springer.com/article/10.1007/s11573-016-0822-8).

Association Rules Mining (ARM) produces Association Rules (AR) from mined Item Sets.
In a typical database (DB), ARM will yield too many ARs to review, forcing the analyst to apply filtration critereon.

This presents a problem when exploring unfamiliar data where the analyst is not yet able to devise effective filtering strategies.
This leads us to explore the potential for visualizations to increase the number of ARs which an analyst can reasonably review and
understand in the course of exploring the data





The package provides multiple, pre-configured visualizations 
It provides multiple, pre-configured visualizations for association rules



 and this 

Included test data obtained from [this site](https://data.world/zpencer/transaction-itemset)


# Installation

## From Github
1. In CLI (with Git setup locally) clone to local directory 
`git clone https://github.com/Mazeofthemind/PyARMViz.git`
2. Navigate into the root directory of the cloned project
`cd PyARMViz`
3. Execute Python build and install (may require sudo or alternate Python psudonym)
`python setup.py install`

## From PyPi (Currently only Testing)
`pip install --index-url https://test.pypi.org/simple/ PyARMViz`