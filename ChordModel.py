import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.ContinuousModel as cm
import ndlib.models.compartments as cpm
import numpy as np

# Network generation
g = nx.erdos_renyi_graph(10, 0.1)
model = cm.ContinuousModel(g)


def generate_opinion(node, graph, status, constants):
    return np.random.uniform(0, 0.5)


initial_status = {
    'Opinion': generate_opinion
}

# Model statuses
model.add_status("Opinion")

condition = cpm.NodeStochastic(1)


#higher value means less social distance
def generate_social_distance(node, graph, status, constants):
    return np.random.uniform(0, 1)


# Model initial status configuration
config = mc.Configuration()
#config.add_model_parameter('diffusion_strenght', 0.1)
config.add_model_parameter('similarity_threshold', 0.3)
#config.add_model_parameter('fraction_infected', 0.1)
for i in g.edges():
    print(i)
    config.add_edge_configuration("social_distance", i, 0.5)

model.set_initial_status(initial_status, config)


def update_opinion(node, graph, status, attributes, constants):
    new_opinion = 0
    for neighbor in graph.neighbors(node):
        neighbor_opinion = status[neighbor]['Opinion']
        print(neighbor_opinion)
        print(status[node]['Opinion'])
        similarity = abs(neighbor_opinion - status[node]['Opinion'])
        print(similarity)
        edge_attributes = g.get_edge_data(node, neighbor)
        neighbour_social_distance = edge_attributes
        print(neighbour_social_distance)

        # print(neighbor_social_distance)

        # # Check if the similarity is above the threshold
        # if similarity <= config.get_model_parameters()['similarity_threshold']:
        #     # Get the edge between the current node and the neighbor
        #     neighbour_social_distance = g.get_edge_data(node, neighbor)['social_distance']
        #     new_opinion += status[node]['Opinion'] + neighbour_social_distance * (neighbor_opinion - status[node]['Opinion'])
    #return status[node]['Opinion'] + new_opinion
    return status[node]['Opinion']


model.add_rule("Opinion", update_opinion, condition)

# Simulation execution

iterations = model.iteration_bunch(5)
print(iterations)
