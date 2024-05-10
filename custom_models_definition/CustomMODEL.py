import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.ContinuousModel as cm
import ndlib.models.compartments as cpm
import numpy as np
import json
import random
import matplotlib.pyplot as plt
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend

from ndlib.viz.mpl.OpinionEvolution import OpinionEvolution

# Network generation
g = nx.erdos_renyi_graph(100, 0.1)
model = cm.ContinuousModel(g)


def generate_opinion(node, graph, status, constants):
    return np.random.uniform(0, 1)


def generate_influence(node, graph, status, constants):
    return np.random.uniform(0, 0.5)


initial_status = {
    'Opinion': generate_opinion,
    'Influence_strength': generate_influence
}

# Model statuses
model.add_status("Opinion")
model.add_status("Influence_strength")

condition = cpm.NodeStochastic(1)

# Model initial status configuration
config = mc.Configuration()
config.add_model_parameter('similarity_threshold', 0.1)

model.set_initial_status(initial_status, config)


def update_opinion(node, graph, status, attributes, constants):
    node_opinion = status[node]['Opinion']
    node_influence_strength = status[node]['Influence_strength']
    valid_neighbors = []
    for neighbor in graph.neighbors(node):
        similarity = abs(node_opinion - status[neighbor]['Opinion'])
        similarity_threshold = model.params['model']['similarity_threshold']
        if similarity <= similarity_threshold:
            valid_neighbors.append(neighbor)

    if len(valid_neighbors) > 0:
        average_neighbor_opinion = sum([status[neighbor]['Opinion'] for neighbor in valid_neighbors]) / len(valid_neighbors)
        new_opinion = node_opinion + node_influence_strength * (average_neighbor_opinion - node_opinion) #* random.uniform(-0.5, 0.5)
        new_opinion = min(1, max(0, new_opinion))  # Limit the value of new_opinion immediately after calculating it
    else:
        new_opinion = status[node]['Opinion']

    print(f"new_opinion for node {node}: {new_opinion}")
    return new_opinion


model.add_rule("Opinion", update_opinion, condition)

# Simulation execution

visualization_config = {
    'plot_interval': 4,
    'plot_variable': 'Opinion',
    'variable_limits': {
        'Opinion': [0, 1]
    },
    'show_plot': True,
    'plot_output': './opinion_evolution.gif',
    'plot_title': 'Opinion evolution simulation',
}
model.configure_visualization(visualization_config)

iterations = model.iteration_bunch(1000)
# print(json.dumps(iterations, indent=1))

# Show animated plot
model.visualize(iterations)

