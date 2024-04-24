"""
https://ndlib.readthedocs.io/en/latest/custom/compartments/NodeStochastic.html

During each rule evaluation, given a node n

if the actual status of n equals the rule initial one
- a random value b in [0,1] will be generated
- if b <= beta then NS is considered satisfied and the status of n changes from initial to final.

Moreover, NS allows to specify a triggering status in order to restrain the compartment evaluation to those nodes that:

1. match the rule initial state, and
2. have at least one neighbors in the triggering status.

"""

#SIR model example

import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm
import json

# Network generation
g = nx.erdos_renyi_graph(1000, 0.1)

# Composite Model instantiation, class CompositeModel is used to create a custom diffusion model using static network
model = gc.CompositeModel(g)

# Model statuses
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Removed")

# Compartment definition, the rate is the beta parameter on the above paragraph
# c1 compartment is triggered only if the node has at least one neighbor in the "Infected" status
c1 = cpm.NodeStochastic(0.02, triggering_status="Infected")
c2 = cpm.NodeStochastic(0.01)

# Rule definition
model.add_rule("Susceptible", "Infected", c1)
model.add_rule("Infected", "Removed", c2)

# Model initial status configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.1)

# Simulation execution
model.set_initial_status(config)
iterations = model.iteration_bunch(6)

for iteration in iterations:
    iteration.pop('status', None)


print(json.dumps(iterations, indent=2))
