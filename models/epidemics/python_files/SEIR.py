import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

# Network topology
g = nx.erdos_renyi_graph(1000, 0.1)

# Model selection
seir_model = ep.SEIRModel(g)

# Model Configuration
config = mc.Configuration()
config.add_model_parameter('beta', 0.01)  # infection rate 1%
config.add_model_parameter('gamma', 0.005)  # recovery rate 0.5%
config.add_model_parameter('alpha', 0.05)  # incubation rate 5%
config.add_model_parameter("fraction_infected", 0.05)  # initial fraction of infected nodes 5%
seir_model.set_initial_status(config)

# Simulation execution
iterations = seir_model.iteration_bunch(200)
seir_trends = seir_model.build_trends(iterations)

viz = DiffusionTrend(seir_model, seir_trends)
viz.plot("seir_trend.png")
viz = DiffusionPrevalence(seir_model, seir_trends)
viz.plot("seir_prev.png")
