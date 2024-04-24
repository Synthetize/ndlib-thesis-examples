"""
https://ndlib.readthedocs.io/en/latest/custom/compartments/NodeNumericalAttribute.html

The rule will take as input the initial node status (Susceptible), the final one (Infected) and the NNA compartment. NNA
 will thus require a probability (beta) of activation.

During each rule evaluation, given a node n and one of its neighbors m

if the actual status of n equals the rule initial
- if attr(n) op attr
- a random value b in [0,1] will be generated
- if b <= beta, then NNA is considered satisfied and the status of n changes from initial to final.

op represent a logic operator and can assume one of the following values: - equality: “==” - less than: “<” - greater
than: “>” - equal or less than: “<=” - equal or greater than: “>=” - not equal to: “!=” - within: “IN”

Parameters:
- attribute: mandatory, the attribute name
- value: mandatory, attribute testing value, the value to be compared with the attribute
- op: mandatory, the logic operator
- probability: not mandatory, the activation probability
- triggering_status: not mandatory, the triggering status
"""

import networkx as nx
import random
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments.NodeNumericalAttribute as na
import json

# Network generation
g = nx.erdos_renyi_graph(1000, 0.1)

# Setting edge attribute
attr = {n: {"Age": random.choice(range(0, 100))} for n in g.nodes()}
nx.set_node_attributes(g, attr)

# Composite Model instantiation
model = gc.CompositeModel(g)

# Model statuses
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Removed")

# Compartment definition
c1 = na("Age", value=18, op="==", probability=0.6)

#in order to change the node status this condition must be satisfied, the node Age attribute must be in the range [20, 25]
#and at least one of the neighbors must be in the Susceptible status. If the condition is satisfied, the node status will
#change with a probability of 0.6
c2 = na("Age", value=[20, 25], op="IN", probability=0.6, triggering_status="Susceptible")

# Rule definition
model.add_rule("Susceptible", "Infected", c1)
model.add_rule("Infected", "Removed", c2)

# Model initial status configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.1)

# Simulation execution
model.set_initial_status(config)
iterations = model.iteration_bunch(100)