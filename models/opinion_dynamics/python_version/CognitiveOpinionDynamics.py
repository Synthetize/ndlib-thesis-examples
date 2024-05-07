import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.opinions as op
from ndlib.viz.mpl.OpinionEvolution import OpinionEvolution

# Network topology
g = nx.erdos_renyi_graph(100, 0.1)

# Model selection
model = op.CognitiveOpDynModel(g)

# Model Configuration
config = mc.Configuration()
config.add_model_parameter("I", 0.15)
config.add_model_parameter("B_range_min", 0)
config.add_model_parameter("B_range_max", 1)
config.add_model_parameter("T_range_min", 0)
config.add_model_parameter("T_range_max", 1)
config.add_model_parameter("R_fraction_negative", 0.2)
config.add_model_parameter("R_fraction_neutral", 0.5)
config.add_model_parameter("R_fraction_positive", 0.3)
config.add_model_parameter('fraction_infected', 0.1)
model.set_initial_status(config)

# Simulation execution
iterations = model.iteration_bunch(200)
trends = model.build_trends(iterations)

viz = OpinionEvolution(model, iterations)
viz.plot("opinion_ev.png")
