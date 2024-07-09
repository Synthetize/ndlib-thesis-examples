import json
import random

import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm
import ndlib.models.epidemics as ep
import numpy as np

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.mpl.TrendComparison import DiffusionTrendComparison


g1 = nx.erdos_renyi_graph(1000, 0.1)
model1 = gc.CompositeModel(g1)

model1.add_status("Susceptible")
model1.add_status("Exposed")
model1.add_status("Infected")
model1.add_status("Removed")
model1.add_status("Vaccinated")
model1.name = "0.2"
config1 = mc.Configuration()
config1.add_model_parameter('fraction_infected', 0.1)
model1.set_initial_status(config1)

c1 = cpm.NodeStochastic(0.05, triggering_status="Infected")
model1.add_rule("Susceptible", "Exposed", c1)

c4 = cpm.NodeStochastic(0.2, triggering_status="Infected")
model1.add_rule("Susceptible", "Vaccinated", c4)

c2 = cpm.NodeStochastic(0.05)
model1.add_rule("Exposed", "Infected", c2)


c3 = cpm.NodeStochastic(0.005)
model1.add_rule("Infected", "Removed", c3)


iterations1 = model1.iteration_bunch(400)
# print(json.dumps(iterations, indent=2))
trends1 = model1.build_trends(iterations1)

# viz = DiffusionTrend(model1, trends)
# viz.plot("sevir_trend.png")
# viz = DiffusionPrevalence(model1, trends)
# viz.plot("sevir_prev.png")
#################################################################

g2 = nx.erdos_renyi_graph(1000, 0.1)
model2 = gc.CompositeModel(g2)
model2.name = "0.03"
model2.add_status("Susceptible")
model2.add_status("Exposed")
model2.add_status("Infected")
model2.add_status("Removed")
model2.add_status("Vaccinated")
config2 = mc.Configuration()
config2.add_model_parameter('fraction_infected', 0.1)
model2.set_initial_status(config2)

c1 = cpm.NodeStochastic(0.05, triggering_status="Infected")
model2.add_rule("Susceptible", "Exposed", c1)

c4 = cpm.NodeStochastic(0.03, triggering_status="Infected")
model2.add_rule("Susceptible", "Vaccinated", c4)

c2 = cpm.NodeStochastic(0.05)
model2.add_rule("Exposed", "Infected", c2)


c3 = cpm.NodeStochastic(0.005)
model2.add_rule("Infected", "Removed", c3)

iterations2 = model2.iteration_bunch(200)
trends2 = model2.build_trends(iterations2)



#################################################################
g3 = nx.erdos_renyi_graph(1000, 0.1)
model3 = gc.CompositeModel(g3)
model3.name = "0.004"
model3.add_status("Susceptible")
model3.add_status("Exposed")
model3.add_status("Infected")
model3.add_status("Removed")
model3.add_status("Vaccinated")
config3 = mc.Configuration()
config3.add_model_parameter('fraction_infected', 0.1)
model3.set_initial_status(config3)

c1 = cpm.NodeStochastic(0.05, triggering_status="Infected")
model3.add_rule("Susceptible", "Exposed", c1)

c4 = cpm.NodeStochastic(0.004, triggering_status="Infected")
model3.add_rule("Susceptible", "Vaccinated", c4)

c2 = cpm.NodeStochastic(0.05)
model3.add_rule("Exposed", "Infected", c2)


c3 = cpm.NodeStochastic(0.005)
model3.add_rule("Infected", "Removed", c3)


iterations = model3.iteration_bunch(200)
trends = model3.build_trends(iterations)



viz = DiffusionTrendComparison([model1], [trends1], ["Susceptible", "Exposed", "Infected", "Removed", "Vaccinated"])
viz.plot("sevir_prev.png")
viz = DiffusionTrendComparison([model1, model2, model3], [trends1, trends2, trends], ["Susceptible"])
viz.plot("sevir_comparison_susceptible.png")
viz = DiffusionTrendComparison([model1, model2, model3], [trends1, trends2, trends], ["Exposed"])
viz.plot("sevir_comparison_exposed.png")
viz = DiffusionTrendComparison([model1, model2, model3], [trends1, trends2, trends], ["Infected"])
viz.plot("sevir_comparison_infected.png")
viz = DiffusionTrendComparison([model1, model2, model3], [trends1, trends2, trends], ["Removed"])
viz.plot("sevir_comparison_removed.png")
viz = DiffusionTrendComparison([model1, model2, model3], [trends1, trends2, trends], ["Vaccinated"])
viz.plot("sevir_comparison_vaccinated.png")


# # Network topology
# g = nx.erdos_renyi_graph(1000, 0.1)
#
# # Model selection
# seir_model = ep.SEIRModel(g)
#
# # Model Configuration
# config = mc.Configuration()
# config.add_model_parameter('beta', 0.05)  # infection rate
# config.add_model_parameter('gamma', 0.005)  # removal rate
# config.add_model_parameter('alpha', 0.05)  # latent period
#
# config.add_model_parameter("tp_rate", 0)  # transmission probability rate
#
# config.add_model_parameter("fraction_infected", 0.1)  # initial fraction of infected nodes
# seir_model.set_initial_status(config)
#
# # Simulation execution
# iterations = seir_model.iteration_bunch(200)
# seir_trends = seir_model.build_trends(iterations)
#
# viz = DiffusionTrend(seir_model, seir_trends)
# viz.plot("seir_trend.png")
# viz = DiffusionPrevalence(seir_model, seir_trends)
# viz.plot("seir_prev.png")
#
#
# viz = DiffusionTrendComparison([seir_model, model], [seir_trends, trends], ["Exposed","Infected"])
# viz.plot("seir_sevir_prev.png")
