import json
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

# Network topology
g = nx.erdos_renyi_graph(1000, 0.1)

# Model selection
model = ep.SIRModel(g)

# Model Configuration
config = mc.Configuration()
config.add_model_parameter('beta', 0.001)
config.add_model_parameter('gamma', 0.01)
config.add_model_parameter("fraction_infected", 0.05)
model.set_initial_status(config)

# Simulation execution
iterations = model.iteration_bunch(200, node_status=False)
trends = model.build_trends(iterations)

viz = DiffusionTrend(model, trends)
viz.plot("sir_trend.png", percentile=50)
viz = DiffusionPrevalence(model, trends)
viz.plot("sir_prev.png")