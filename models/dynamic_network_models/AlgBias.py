import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.opinions as op
from ndlib.viz.mpl.OpinionEvolution import OpinionEvolution
# Network topology
g = nx.erdos_renyi_graph(1000, 0.1)

# Model selection
model = op.AlgorithmicBiasModel(g)

# Model configuration
config = mc.Configuration()
config.add_model_parameter("epsilon", 0.7)
config.add_model_parameter("gamma", 0.6)
model.set_initial_status(config)

# Simulation execution
iterations = model.iteration_bunch(200)

viz = OpinionEvolution(model, iterations)
viz.plot("opinion_ev_2.png")