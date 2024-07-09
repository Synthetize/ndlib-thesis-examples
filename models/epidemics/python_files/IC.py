import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import random
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

# Network topology
g = nx.erdos_renyi_graph(1000, 0.05)

# Model selection
model = ep.IndependentCascadesModel(g)

# Model Configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.05)

# Setting the edge parameters
threshold = 0.9
for e in g.edges():
    config.add_edge_configuration("threshold", e, random.choice([0.05, 0.1]))


model.set_initial_status(config)

# Simulation execution
iterations = model.iteration_bunch(10)
trends = model.build_trends(iterations)
viz = DiffusionTrend(model, trends)
viz.plot("ic_trend.png")
viz = DiffusionPrevalence(model, trends)
viz.plot("ic_prev.png")