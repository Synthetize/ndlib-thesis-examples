"""
Edge Stochastic compartments are used to evaluate stochastic events attached to network edges.

The rule will take as input the initial node status (Susceptible), the final one (Infected) and the ES compartment.
ES will thus require a probability (beta) of edge activation and a triggering status. In advanced scenarios, where the
probability threshold vary from edge to edge, it is possible to specify it using the model configuration object.

During each rule evaluation, given a node n and one of its neighbors m if the actual status of n equals the rule initial
one and the one of m equals the triggering one
- a random value b in [0,1] will be generated
- if b <= beta then ES is considered satisfied and the status of n changes from initial to final.

Parameters
- threshold: mandatory, the probability of edge activation
- triggering_status: not mandatory, the status of the neighbor node that triggers the edge activation.
"""
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments.EdgeStochastic as es
import numpy as np


def homogeneous_threshold_value():
    # Network generation
    g = nx.erdos_renyi_graph(1000, 0.1)

    # Composite Model instantiation
    model = gc.CompositeModel(g)

    # Model statuses
    model.add_status("Susceptible")
    model.add_status("Infected")
    model.add_status("Removed")

    # Compartment definition
    c1 = es.EdgeStochastic(0.02, triggering_status="Infected")

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
    model.add_status("Removed")

    # Compartment definition
    c1 = es.EdgeStochastic(triggering_status="Infected")

    # Rule definition
    model.add_rule("Susceptible", "Infected", c1)

    # Model initial status configuration
    config = mc.Configuration()

    # Threshold specs
    for e in g.edges():
        config.add_edge_configuration("threshold", e, np.random.random_sample())

    config = mc.Configuration()
    config.add_model_parameter('fraction_infected', 0.1)

    # Simulation execution
    model.set_initial_status(config)
    iterations = model.iteration_bunch(100)


homogeneous_threshold_value()
heterogeneous_threshold_value()
