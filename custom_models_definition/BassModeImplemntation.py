import networkx as nx
import ndlib.models.ModelConfig as mc
import BassModel as bmi
import json
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence


g = nx.erdos_renyi_graph(100, 0.1)
model = bmi.BassModel(g)
config = mc.Configuration()
config.add_model_parameter('p', 0.01)
config.add_model_parameter('q', 0.3)
config.add_model_parameter('fraction_infected', 0.1)
model.set_initial_status(config)
iterations = []
for i in range(0, 100):
    iteration = model.iteration()
    iterations.append(iteration)

trends = model.build_trends(iterations)
print(json.dumps(trends, indent=1))


viz = DiffusionTrend(model, trends)
viz.plot("bass_trend.png")


viz = DiffusionPrevalence(model, trends)
viz.plot("bass_prevalence.png")
