import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.opinions as op
from ndlib.viz.mpl.OpinionEvolution import OpinionEvolution

# mMean field scenario
g = nx.complete_graph(100)

# Algorithmic Bias model
model = op.AlgorithmicBiasModel(g)

# Model configuration
config = mc.Configuration()
config.add_model_parameter("epsilon", 0.32)
config.add_model_parameter("gamma", 0)
model.set_initial_status(config)

# Simulation execution
iterations = model.iteration_bunch(20)

viz = OpinionEvolution(model, iterations)
viz.plot("opinion_ev.pdf")