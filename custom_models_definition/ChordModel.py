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
g = nx.erdos_renyi_graph(50, 0.1)
model = cm.ContinuousModel(g)


def generate_opinion(node, graph, status, constants):
    return np.random.uniform(0, 200)


initial_status = {
    'Opinion': generate_opinion
}

# Model statuses
model.add_status("Opinion")

condition = cpm.NodeStochastic(1)


#higher value means less social distance
def generate_social_distance():
    return random.randint(1, 5)


# Model initial status configuration
config = mc.Configuration()
config.add_model_parameter('similarity_threshold', 0.2)


social_dist = 0.2
for i in g.edges():
    config.add_edge_configuration("social_distance", i, generate_social_distance())

model.set_initial_status(initial_status, config)


def find_edge_social_distance(node, neighbor):
    edges = model.params['edges']['social_distance']
    if (node, neighbor) in edges:
        return edges[(node, neighbor)]
    elif (neighbor, node) in edges:
        return edges[(neighbor, node)]
    else:
        return 'not found'


def update_opinion(node, graph, status, attributes, constants):
    valid_neighbors = []
    node_opinion = status[node]['Opinion']

    for neighbor in graph.neighbors(node):
        neighbor_opinion = status[neighbor]['Opinion']
        similarity = abs(neighbor_opinion - node_opinion)
        # Check if the similarity is above the threshold
        if similarity <= config.get_model_parameters()['similarity_threshold']:
            # Get the edge between the current node and the neighbor
            valid_neighbors.append(neighbor)

    # Inverse distance weighted
    if len(valid_neighbors) == 0:
        return node_opinion

    inverted_sum_social_distance = 0
    weighted_sum_neighbor_opinions = 0
    for neighbor in valid_neighbors:
        neighbor_opinion = status[neighbor]['Opinion']
        inverted_social_distance = 1 / find_edge_social_distance(node, neighbor)
        inverted_sum_social_distance += inverted_social_distance
        weighted_sum_neighbor_opinions += neighbor_opinion * inverted_social_distance

    print('Inverse sum social distance: ', inverted_sum_social_distance)
    updated_opinion = node_opinion + weighted_sum_neighbor_opinions / inverted_sum_social_distance
    return updated_opinion


model.add_rule("Opinion", update_opinion, condition)

# Simulation execution

visualization_config = {
    'plot_interval': 2,
    'plot_variable': 'Opinion',
    'variable_limits': {
        'Opinion': [0, 200]
    },
    'show_plot': True,
    'plot_output': './opinion_evolution.gif',
    'plot_title': 'Opinion evolution simulation',
}
model.configure_visualization(visualization_config)

iterations = model.iteration_bunch(100)
print(json.dumps(iterations, indent=1))

# Show animated plot
model.visualize(iterations)

