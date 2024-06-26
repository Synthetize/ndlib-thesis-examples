"""
The rule will take as input the initial node status (Susceptible), the final one (Infected) and the NT compartment. NT will thus require a threshold (beta) of activation and a triggering status.

During each rule evaluation, given a node n if the actual status of n equals the rule initial one
- let b identify the ratio of n neighbors in the triggering status
- if b >= beta then NS is considered satisfied and the status of n changes from initial to final.

Parameters:
- threshold: not mandatory, the threshold value
- triggering_status: mandatory, the triggering status

"""

import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments.NodeThreshold as ns
import numpy as np


def homogeneous_threshold_value():
    # Network generation
    g = nx.erdos_renyi_graph(1000, 0.1)

    # Composite Model instantiation
    model = gc.CompositeModel(g)

    # Model statuses
    model.add_status("Susceptible")
    model.add_status("Infected")

    # Compartment definition
    c1 = ns.NodeThreshold(0.1, triggering_status="Infected")

    # Rule definition
    model.add_rule("Susceptible", "Infected", c1)

    # Model initial status configuration
    config = mc.Configuration()
    config.add_model_parameter('fraction_infected', 0.1)

    # Simulation execution
    model.set_initial_status(config)
    iterations = model.iteration_bunch(100)
    return iterations


def heterogeneous_threshold_value():
    # Network generation
    g = nx.erdos_renyi_graph(1000, 0.1)

    # Composite Model instantiation
    model = gc.CompositeModel(g)

    # Model statuses
    model.add_status("Susceptible")
    model.add_status("Infected")

    # Compartment definition
    c1 = ns.NodeThreshold(triggering_status="Infected")

    # Rule definition
    model.add_rule("Susceptible", "Infected", c1)

    # Model initial status configuration
    config = mc.Configuration()

    # Threshold specs, for each node in the network a threshold value is randomly assigned between 0 and 1
    for i in g.nodes():
        config.add_node_configuration("threshold", i, np.random.random_sample())

    config = mc.Configuration()
    config.add_model_parameter('fraction_infected', 0.1)

    # Simulation execution
    model.set_initial_status(config)
    iterations = model.iteration_bunch(100)
    return iterations
