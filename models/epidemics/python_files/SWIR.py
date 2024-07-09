import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

# Network topology
g = nx.erdos_renyi_graph(1000, 0.05)

# Model selection
model = ep.SWIRModel(g)

# Model Configuration
cfg = mc.Configuration()
cfg.add_model_parameter('kappa', 0.01)
cfg.add_model_parameter('mu', 0.005)
cfg.add_model_parameter('nu', 0.05)
cfg.add_model_parameter("fraction_infected", 0.05)
model.set_initial_status(cfg)

# Simulation execution
iterations = model.iteration_bunch(200)
trends = model.build_trends(iterations)
viz = DiffusionTrend(model, trends)
viz.plot("swir_trend.png")
viz = DiffusionPrevalence(model, trends)
viz.plot("swir_prev.png")

