import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence
import json

# Network topology
g = nx.erdos_renyi_graph(1000, 0.1)

# Model selection
model = ep.GeneralisedThresholdModel(g)

# Model Configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.1)
config.add_model_parameter('tau', 5)
config.add_model_parameter('mu', 5)

# Setting node parameters
threshold = 0.25
for i in g.nodes():
    config.add_node_configuration("threshold", i, threshold)

model.set_initial_status(config)

# Simulation execution
iterations = model.iteration_bunch(200)
print(json.dumps(iterations, indent=2))

viz = DiffusionTrend(model, iterations)
viz.plot("gt_trend.png")
viz = DiffusionPrevalence(model, iterations)
viz.plot("gt_prev.png")
