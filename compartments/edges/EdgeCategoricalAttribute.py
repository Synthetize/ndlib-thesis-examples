"""
The rule will take as input the initial node status (Susceptible), the final one (Infected) and the ECA compartment.
ECA will thus require a probability (beta) of activation.

During each rule evaluation, given a node n and one of its neighbors mif the actual status of n equals the rule initial
- if attr(n,m) == attr
- a random value b in [0,1] will be generated
- if b <= beta, then ECA is considered satisfied and the status of n changes from initial to final.

Moreover, ECA allows to specify a triggering status in order to restrain the compartment evaluation to those nodes that:
- match the rule initial state, and
- have at least one neighbors in the triggering status.

Parameters:
- attribute: mandatory, the attribute name
- value: mandatory, the attribute testing value
- probability: not mandatory, the event probability
- triggering_status: not mandatory, the triggering status
"""

import networkx as nx
import random
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
from ndlib.models.compartments import EdgeCategoricalAttribute
import json

# Network generation
g = nx.erdos_renyi_graph(300, 0.1)

# Setting edge attribute
attr = {e: {"type": random.choice(['co-worker', 'family'])} for e in g.edges()}
nx.set_edge_attributes(g, attr)

# Composite Model instantiation
model = gc.CompositeModel(g)

# Model statuses
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Recovered")

# Compartment definition
#all nodes with co-worker edge will be infected with probability 0.6
c1 = EdgeCategoricalAttribute("type", "co-worker", probability=0.6)
#all nodes with family edge will be recovered with probability 0.6 only if they have
# at least one neighbor in the Susceptible status
c2 = EdgeCategoricalAttribute("type", "family", probability=0.6, triggering_status="Susceptible")

# Rule definition
model.add_rule("Susceptible", "Infected", c1)
model.add_rule("Infected", "Recovered", c2)

# Model initial status configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.1)

# Simulation execution
model.set_initial_status(config)
iterations = model.iteration_bunch(10)

for iteration in iterations:
    iteration.pop('status', None)

print(json.dumps(iterations, indent=2))