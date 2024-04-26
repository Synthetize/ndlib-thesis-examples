import networkx as nx
import random
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as na

# Network generation
g = nx.erdos_renyi_graph(1000, 0.1)

# Setting edge attribute
attr = {(u, v): {"weight": int((u + v) % 10)} for (u, v) in g.edges()}
nx.set_edge_attributes(g, attr)

# Composite Model instantiation
model = gc.CompositeModel(g)

# Model statuses
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Removed")

# Compartment definition
c1 = na.EdgeNumericalAttribute("weight", value=4, op="==", probability=0.6)
c2 = na.EdgeNumericalAttribute("weight", value=(3, 6), op="IN", probability=0.6, triggering_status="Susceptible")

# Rule definition
model.add_rule("Susceptible", "Infected", c1)
model.add_rule("Infected", "Recovered", c2)

# Model initial status configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0)

# Simulation execution
model.set_initial_status(config)
iterations = model.iteration_bunch(100)
