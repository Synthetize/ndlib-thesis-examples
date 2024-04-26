"""
The rule will take as input the initial node status (Susceptible), the final one (Infected) and the CD compartment. CD will thus require a countdown name (cn) and the number of iterations (t) before activation.

During each rule evaluation, given a node n

-if the actual status of n equals the rule initial one
    - if the node does not have an associated countdown cn initialize it to t
    - else
        - if cn(t) > t decrement cn(t)
        - if cn(t) <= t then CD is considered satisfied and the status of n changes from initial to final.

Parameters:
- name: mandatory, the countdown name
- iterations: mandatory, duration of the countdown

"""

import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cd
import json

# Network generation
g = nx.erdos_renyi_graph(1000, 0.1)

# Composite Model instantiation
model = gc.CompositeModel(g)

# Model statuses
model.add_status("Susceptible")
model.add_status("Infected")

# Compartment definition
c1 = cd.CountDown("incubation", iterations=3)

# Rule definition
model.add_rule("Susceptible", "Infected", c1)

# Model initial status configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.1)

# Simulation execution
model.set_initial_status(config)
iterations = model.iteration_bunch(10)

for iteration in iterations:
    iteration.pop('status', None)

print(json.dumps(iterations, indent=2))