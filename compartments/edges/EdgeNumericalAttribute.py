
import networkx as nx
import random
import json
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
from ndlib.models.compartments import EdgeNumericalAttribute

# Network generation
g = nx.erdos_renyi_graph(1000, 0.1)

# Setting edge attribute
attr = {(u, v): {"weight": int((u+v) % 10)} for (u, v) in g.edges()}
nx.set_edge_attributes(g, attr)

# Composite Model instantiation
model = gc.CompositeModel(g)

# Model statuses
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Removed")

# Compartment definition
c1 = EdgeNumericalAttribute("weight", value=5, op="==", probability=0.6)
c2 = EdgeNumericalAttribute("weight", value=[3, 6], op="IN", probability=0.6, triggering_status="Susceptible")
# Rule definition
model.add_rule("Susceptible", "Infected", c1)
model.add_rule("Infected", "Removed", c2)

# Model initial status configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.1)

# Simulation execution
model.set_initial_status(config)
iterations = model.iteration_bunch(10)

for iteration in iterations:
    iteration.pop('status', None)

print(json.dumps(iterations, indent=2))