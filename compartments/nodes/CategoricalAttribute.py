"""
https://ndlib.readthedocs.io/en/latest/custom/compartments/NodeCategoricalAttribute.html

Susceptible->Infected that requires a that the susceptible node express a specific value of an internal attribute, attr,
to be satisfied (e.g. “Sex”=”male”).

The rule will take as input the initial node status (Susceptible), the final one (Infected) and the NCA compartment.
NCA will thus require a probability (beta) of activation.

During each rule evaluation, given a node n

f the actual status of n equals the rule initial one
- a random value b in [0,1] will be generated
- if b <= beta and attr(n) == attr, then NCA is considered satisfied and the status of n changes from initial to final.

Parameters:
- attribute: mandatory, the attribute name
- value: mandatory, the attribute testing value
- probability: not mandatory, the event probability
- triggering_status: not mandatory, the triggering status (not mentioned in the documentation)
"""

import networkx as nx
import random
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm
import json

# Network generation
g = nx.erdos_renyi_graph(100, 0.1)

# Setting node attribute
attr = {n: {"Sex": random.choice(['male', 'female'])} for n in g.nodes()}
nx.set_node_attributes(g, attr)

# Composite Model instantiation
model = gc.CompositeModel(g)

# Model statuses
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Removed")


# Compartment definition
# if the node has the attribute sex equal to male, and has at least one neighbor in the infected status
# then the node will change its status from Susceptible to Infected with a probability of 60%
c1 = cpm.NodeCategoricalAttribute("Sex", "male", probability=0.6, triggering_status="Infected")

# Rule definition
model.add_rule("Susceptible", "Infected", c1)

# Model initial status configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.05)

# Simulation execution
model.set_initial_status(config)
iterations = model.iteration_bunch(10)


# for iteration in iterations:
#     iteration.pop('status', None)

for iteration in iterations:
    print('-'*20)
    print("Iteration", iteration['iteration'], 'Changed statuses:')
    for node_id, status in iteration['status'].items():
        sex = g.nodes[node_id]['Sex']
        print(f"Node {node_id}: Sex = {sex}, Status = {status}")


#print(json.dumps(iterations, indent=2))

