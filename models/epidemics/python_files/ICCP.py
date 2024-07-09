import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import random
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence


# Network topology
g = nx.erdos_renyi_graph(2000, 0.05)

# Model selection
model = ep.ICEPModel(g)

# Model Configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.005)
config.add_model_parameter('permeability', 0.2)


# Setting the edge threshold
for e in g.edges():
    config.add_edge_configuration("threshold", e, random.choice([0.1, 0.2, 0.3]))

# Setting the node community
for node in g.nodes():
    config.add_node_configuration("com", node, random.choice(["A", "B", "C"]))

model.set_initial_status(config)

# Simulation execution
iterations = model.iteration_bunch(15)
trends = model.build_trends(iterations)
viz = DiffusionTrend(model, trends)
viz.plot("trend.png")
viz = DiffusionPrevalence(model, trends)
viz.plot("prev.png")