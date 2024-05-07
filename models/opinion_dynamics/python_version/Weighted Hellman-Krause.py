import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.opinions as opn
from ndlib.viz.mpl.OpinionEvolution import OpinionEvolution

# Network topology
g = nx.erdos_renyi_graph(1000, 0.1)

# Model selection
model = opn.WHKModel(g)

# Model Configuration
config = mc.Configuration()
config.add_model_parameter("epsilon", 0.15)

# Setting the edge parameters
weight = 0.2
if isinstance(g, nx.Graph):
    edges = g.edges
else:
    edges = [(g.vs[e.tuple[0]]['name'], g.vs[e.tuple[1]]['name']) for e in g.es]

for e in edges:
    config.add_edge_configuration("weight", e, weight)


model.set_initial_status(config)

# Simulation execution
iterations = model.iteration_bunch(20)


viz = OpinionEvolution(model, iterations)
viz.plot("opinion_WHK.png")
