import plotly.graph_objects as go
import networkx as nx
import numpy as np

from PyARMViz import Rule

from typing import List
import itertools

import logging

import math

def metadata_scatter_plot(rules:List, allow_compound_flag:bool=False):
    '''
    Visualizes the distribution of Association Rule Confidence, Support and Lift in the form of a
    Plotly scatterplot
    '''
    id_list = []
    confidence_list = []
    lift_list = []
    support_list = []
    
    for rule in rules:
        #Discard compound rules (either pre or antecedents) if indicated 
        if allow_compound_flag == False:
            if len(rule.rhs) > 1 or len(rule.lhs) > 1:
                continue

        confidence_list.append(rule.confidence)
        lift_list.append(rule.lift)
        support_list.append(rule.support)
        hover_text = "{} => {}, Lift: {}".format(rule.lhs, rule.rhs, rule.lift)
        id_list.append(hover_text)
        
    colorbar=dict(
        tick0=0,
        dtick=1
    )
    
    
    fig = go.Figure(data=go.Scatter(x=support_list, y=confidence_list, text = id_list, mode='markers', marker={'color': lift_list, 'colorscale': "purp", 'colorbar':{'title': 'Lift'}},))
    fig.update_layout(title="Association Rules Strength Distribution", xaxis_title="Support", yaxis_title="Confidence", xaxis={'autorange':'reversed'},)
    fig.show()
    return fig

def adjacency_parallel_category_plot(rules:List):
    '''
        Visualizes the antecedents and consequents of each association rules by drawing lines
        representing each rule across identical vertical axes representing the potential items
        in the entire dataset
        
        Similar to parallel coordinate plot but more readible for small numbers of categorical
        points
    '''
    unique_entities_by_axis_count = []
    rules_by_axis_count = []
    for rule in rules:
        axis_required = len(rule.lhs) + 1 

        #Filter out rules with multiple consequents
        #TODO consider allowing multiple consequents
        if len(rule.rhs) == 1:
            #If the rules_by_axis_count list lacks a slot for the current number of antacedents, add them
            while len(rules_by_axis_count) < axis_required - 1:
                rules_by_axis_count.append([])
                unique_entities_by_axis_count.append(set())
            
            #Add the rule and the entities found in its atecedents and consequents to their respective structure
            rules_by_axis_count[axis_required - 2].append(rule)
            unique_entities_by_axis_count[axis_required - 2] = unique_entities_by_axis_count[axis_required - 2].union(set(rule.lhs), set(rule.rhs))

    axis_counter = 2
    for rules, unique_entities in zip(rules_by_axis_count, unique_entities_by_axis_count): 
        line_color = list(map(lambda rule: round(rule.confidence, 2), rules))
    
        dimensions = _parallel_category_builder(rules, axis_counter)
        fig = go.Figure(data=
            go.Parcats(
                dimensions = dimensions,
            )
        )

        fig.update_layout(
            plot_bgcolor = 'white',
            paper_bgcolor = 'white'
        )

        fig.show()    
        axis_counter += 1    
    
def adjacency_parallel_coordinate_plot(rules:List):
    '''
        Visualizes the antecedents and consequents of each rule by drawing lines
        representing each rule across identical vertical axis representing the
        potential items in the set
        
        Has the advantage of making it easier to visualize compound rules over
        scatterplots
    '''
    
    #These two structures track the rules and entities therein based on the number of antecedents/consequents involved
    #Allows us to visualize each number separately in a parallel coordinate graph
    #Note these are indexed 0->2 axis on (no association rule can have less then 2)
    unique_entities_by_axis_count = []
    rules_by_axis_count = []
    for rule in rules:
        axis_required = len(rule.lhs) + 1 
            
        #Filter out rules with multiple consequents
        #TODO consider allowing multiple consequents
        if len(rule.rhs) == 1:
            #If the rules_by_axis_count list lacks a slot for the current number of antacedents, add them
            while len(rules_by_axis_count) < axis_required - 1:
                rules_by_axis_count.append([])
                unique_entities_by_axis_count.append(set())
            
            #Add the rule and the entities found in its atecedents and consequents to their respective structure
            rules_by_axis_count[axis_required - 2].append(rule)
            unique_entities_by_axis_count[axis_required - 2] = unique_entities_by_axis_count[axis_required - 2].union(set(rule.lhs), set(rule.rhs))

    
    axis_counter = 2
    for rules, unique_entities in zip(rules_by_axis_count, unique_entities_by_axis_count): 
        unique_entities = list(unique_entities)
        unique_entities = _parallel_coord_axis_optimizer(rules, unique_entities, axis_counter)
    
        line_color = list(map(lambda rule: round(rule.confidence, 2), rules))
    
        dimensions = _paracoord_builder(rules, unique_entities, axis_counter)
        fig = go.Figure(data=
            go.Parcoords(
                line = dict(color = line_color,
                           colorscale = [[0,'white'], [1,'red']]),
                dimensions = dimensions
            )
        )

        fig.update_layout(
            plot_bgcolor = 'white',
            paper_bgcolor = 'white'
        )

        fig.show()    
        axis_counter += 1

def _parallel_coord_axis_optimizer(rules:List, unique_entities:List, axis_count:int):
    '''
        Accepts the rules, a list of the entities to be included in each axis, and the number of axis
        
        Runs simulations to identify the optimum configuration of entities on those axis in order to
        avoid crossings
        
        Returns that optimum configuration as an ordered list
    '''
    #Generate all possible combinations of entities on the axis and calculate their expected crossings
    max_iterations = 1000
    cross_counts = []
    permutations = set()
    
    iteration_counter = 0
    maximum_permutations = math.factorial(len(unique_entities))
    while len(permutations) < maximum_permutations and len(permutations) < max_iterations:
        perm = np.random.permutation(unique_entities)
        permutations.add(tuple(perm))
        iteration_counter += 1
    permutations = list(permutations)
    logging.info("Finished computing {} random axis entity arrangement permutations in {} iterations".format(len(permutations), iteration_counter))
    
    for permutation in permutations:
        cross_count = _parallel_coord_cross_counter(rules, permutation, axis_count)
        cross_counts.append(cross_count)
        logging.debug("Counted {} crossings for {}".format(cross_count, permutation))
    
    optimum_cross_count = min(cross_counts)
    optimum_axis_configuration = permutations[cross_counts.index(optimum_cross_count)]
    logging.info("Found optimum solution {} with {} crossings".format(optimum_axis_configuration, min(cross_counts)))
    return optimum_axis_configuration

def _parallel_coord_cross_counter(rules:List, unique_entities_permutation:List, axis_count:int):
    '''
        Accepts an axis configuration and computes the number of crossings across all consecutive
        axis pairs in order to determine the overall number of crossings
        
        Note this approach works because the entity order is synchronized on all axis
        
        Returns the number of crossings
    '''
    
    #Iterates through consecutive axis pairs
    cross_count = 0
    for axis_index in range(0, axis_count - 1):
        #Generate all possible pairs of relevant rules and test if they cross for this axis
        combinations = itertools.combinations(rules, 2)
        for rule1, rule2 in combinations:
            if axis_index < (axis_count - 1) - 1:
                src_axis_position1 = rule1.lhs[axis_index]
                dst_axis_position1 = rule2.lhs[axis_index]
                src_axis_position2 = rule1.lhs[axis_index + 1]
                dst_axis_position2 = rule2.lhs[axis_index + 1]
            #Handles the final axis pair which involves the consequent
            else:
                src_axis_position1 = rule1.lhs[axis_index]
                dst_axis_position1 = rule2.lhs[axis_index]
                src_axis_position2 = rule1.rhs[0]
                dst_axis_position2 = rule2.rhs[0]
            
            src_delta = unique_entities_permutation.index(src_axis_position1) - unique_entities_permutation.index(src_axis_position2)
            dst_delta = unique_entities_permutation.index(dst_axis_position1) - unique_entities_permutation.index(dst_axis_position2)
            
            #A cross exists only if the edges terminations swap being above/below the other on each side
            if src_delta < 0 and dst_delta > 0:
                cross_count += 1
            elif src_delta > 0 and dst_delta < 0:
                cross_count += 1        
    return cross_count
    
def _paracoord_builder(rules:List, unique_entities:List, axis_count:int):
    '''
        Helper function to generate list of unique entities across all provided rules to build axis_index 
    '''
    axis_objects = []
    for axis_index in range(0,axis_count):
        if axis_index < axis_count - 1:
            antacedent_count = abs(axis_index - (axis_count - 1))
            label = "Antacedent {}".format(antacedent_count)
        else: 
            label = "Consequent"
            
            
        #Iterate through rules, identify those relevant to that axis_index, and collect their values
        values = []
        for rule in rules:
            #For all but the last axis_index, pull value from the left hand antacedents
            if axis_index < axis_count - 1:
                #If available, pull out the antacedent for this axis_index, otherwise add placeholder
                if axis_index > len(rule.lhs) - 1:
                    values.append(None)
                else:
                    #Note field contains the index of the value on the axis_index
                    values.append(unique_entities.index(rule.lhs[axis_index]))
            #Otherwise add the right hand consequent
            else:
                #Note field contains the index of the value on the axis_index
                values.append(unique_entities.index(rule.rhs[0]))
            
        #Compose the plot object for this axis_index
        axis_object = dict(
            range = [0, len(unique_entities)], 
            label=label,
            ticktext=unique_entities,
            tickvals=list(range(0, len(unique_entities))), 
            values=values
        )
        axis_objects.append(axis_object)
    
    return axis_objects

def _parallel_category_builder(rules:List, axis_count:int):
    '''
        Helper function to generate list of unique entities across all provided rules to build axis_index 
    '''
    axis_objects = []
    for axis_index in range(0,axis_count):
        if axis_index < axis_count - 1:
            antacedent_count = abs(axis_index - (axis_count - 1))
            label = "Antacedent {}".format(antacedent_count)
        else: 
            label = "Consequent"
            
        #Iterate through rules, identify those relevant to that axis_index, and collect their values
        values = []
        for rule in rules:
            #For all but the last axis_index, pull value from the left hand antacedents
            if axis_index < axis_count - 1:
                #If available, pull out the antacedent for this axis_index, otherwise add placeholder
                if axis_index > len(rule.lhs) - 1:
                    values.append(None)
                else:
                    #Note field contains the index of the value on the axis_index
                    values.append(rule.lhs[axis_index])
            #Otherwise add the right hand consequent
            else:
                #Note field contains the index of the value on the axis_index
                values.append(rule.rhs[0])
        #Compose the plot object for this axis_index
        axis_object = dict(
            label=label,
            values=values,
        )
        axis_objects.append(axis_object)
    
    return axis_objects

def adjacency_graph_plotly(rules:Rule):
    '''
        This is the plotly version of the 
    '''
    graph = _adjacency_graph_generator(rules)
    pos = nx.spring_layout(graph, iterations=100)
    
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        src_node_ind = edge[0]
        dst_node_ind = edge[1]
        x0, y0 =  pos[src_node_ind]
        x1, y1 =  pos[dst_node_ind]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_text = []
    node_x = []
    node_y = []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)


    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    fig = go.Figure(data=[edge_trace, node_trace],
         layout=go.Layout(
            title='<br>Network graph made with Python',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002 ) ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            )
    fig.show()

def adjacency_graph_gephi(rules:List[Rule], output_path:str=None):
    '''
    Uses networkX to produce a directed graph representation of the generated
    association rules (both 1-to-1 and compound).
    
    Either displays the resulting graph in the browser with Plotly or 
    export it as a graphml file to be viewed in a program like Gephi
    '''
    graph = _adjacency_graph_generator(rules)
    nx.write_gexf(graph, output_path)
    logging.debug("Output rule graph to {}".format(output_path))
    return graph
    
def _adjacency_graph_generator(rules:List[Rule]):
    '''
        Helper function to generate a directional network graph using the antecedents and
        precedents of each Association Rule. This allows the user to discern higher level
        structures such as chains and hubs which are formed by adjacent rules. 
        
        The resulting graph can then be visualized through a variety of means 
    '''
    graph = nx.DiGraph()
    for index, rule in enumerate(rules):
        graph.add_node (index, Weight=int(rule.confidence*10), type="Association_Rule")

        for entity in rule.lhs:
            graph.add_node(entity, Weight=1, type="Entity")
            graph.add_edge(entity, index, Normalized_Lift=int(rule.lift*10))
            
        for entity in rule.rhs:
            graph.add_node(entity, Weight=1, type="Entity")
            graph.add_edge(index, entity, Normalized_Lift=int(rule.lift*10))
    
    logging.debug("Generated NetworkX graph for {} rules with {} nodes".format(len(rules), len(graph.nodes)))
    return graph
    


def adjacency_scatter_plot(rules:List[Rule], notebook_flag:bool = False):
    '''
    Generates a plot showing the distribution of association rules in terms of association
    rules between antecedent and consequent entities, support and confidence
    
    Visulizes this plot as a Plotly scattergraph and views it in the browser
    '''
    unique_values = set()
    x_axis = []
    y_axis = []
    strength = []
    for index, rule in enumerate(rules):
        x_axis.append(str(rule.rhs))
        y_axis.append(str(rule.lhs))
        strength.append(20 * rule.confidence)
        unique_values.add(str(rule.rhs))
        unique_values.add(str(rule.lhs))
        
    #Generate distance matrix view
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_axis,
        y=y_axis,
        mode="markers",
        marker = {'size':strength},
        name='Association rules',
    ))
    
    fig.show()
    return fig