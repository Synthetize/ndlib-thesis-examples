"""
The rule will take as input the initial node status (Susceptible), the final one (Infected) and the NNV compartment.
NNV will thus require a probability (beta) of activation.

During each rule evaluation, given a node n and one of its neighbors m if the actual status of n equals the rule initial
- if var(n) op var(n) (where var(n) = attr(n) or status(n))
- a random value b in [0,1] will be generated
- if b <= beta, then NNV is considered satisfied and the status of n changes from initial to final.

op represent a logic operator and can assume one of the following values: - equality: “==” - less than: “<” - greater
than: “>” - equal or less than: “<=” - equal or greater than: “>=” - not equal to: “!=” - within: “IN”

Moreover, NNV allows to specify a triggering status in order to restrain the compartment evaluation to those nodes that:

- match the rule initial state, and
- have at least one neighbors in the triggering status.

Parameters:
- variable: mandatory, the of the variable to compare
- variable_type: mandatory, the type of the variable to compare (status or attribute)
- value: mandatory, the value to be compared with the variable
- value_type: mandatory, the type of the value to be compared with the variable (status or attribute)
- op: mandatory, the logic operator
- probability: not mandatory, the activation probability
- triggering_status: not mandatory, the triggering status

"""

import networkx as nx
import random
from ndlib.models.CompositeModel import CompositeModel
from ndlib.models.ContinuousModel import ContinuousModel
from ndlib.models.compartments.enums.NumericalType import NumericalType
from ndlib.models.compartments.NodeNumericalVariable import NodeNumericalVariable
import ndlib.models.ModelConfig as mc


def composite_model():
    # Network generation
    g = nx.erdos_renyi_graph(1000, 0.1)

    # Setting edge attribute
    attr = {n: {"Age": random.choice(range(0, 100)), "Friends": random.choice(range(0, 100))} for n in g.nodes()}
    nx.set_node_attributes(g, attr)

    # Composite Model instantiation
    model = CompositeModel(g)

    # Model statuses
    model.add_status("Susceptible")
    model.add_status("Infected")
    model.add_status("Removed")

    # Compartment definition
    condition = NodeNumericalVariable('Friends', var_type=NumericalType.ATTRIBUTE, value=18, op='>')
    condition2 = NodeNumericalVariable('Age', var_type=NumericalType, value='Friends',
                                       value_type=NumericalType.ATTRIBUTE, op='<')

    # Rule definition
    model.add_rule("Susceptible", "Infected", condition)
    model.add_rule("Infected", "Removed", condition2)

    # Model initial status configuration
    config = mc.Configuration()
    config.add_model_parameter('fraction_infected', 0.05)

    # Simulation execution
    model.set_initial_status(config)
    iterations = model.iteration_bunch(100)
    return iterations


def continuous_model():
    # Network generation
    g = nx.erdos_renyi_graph(1000, 0.1)

    # Continuous Model instantiation
    model = ContinuousModel(g)

    # Model statuses
    model.add_status("Susceptible")
    model.add_status("Infected")
    model.add_status("Removed")

    # Setting node status values, in the continuous model the status values are continuous values in the range [0,1]
    status_values = {n: {"Susceptible": random.random(), "Infected": random.random(), "Removed": random.random()} for n
                     in g.nodes()}
    nx.set_node_attributes(g, status_values)

    # Compartment definition, id the node status value is greater than 0.5 the condition is satisfied
    condition = NodeNumericalVariable('Infected', var_type=NumericalType.STATUS, value=0.5, op='>')
    condition2 = NodeNumericalVariable('Removed', var_type=NumericalType.STATUS, value=0.5, op='>')

    # Rule definition
    model.add_rule("Susceptible", "Infected", condition)
    model.add_rule("Infected", "Removed", condition2)

    # Model initial status configuration
    config = mc.Configuration()
    config.add_model_parameter('fraction_infected', 0.05)

    # Simulation execution
    model.set_initial_status(config)
    iterations = model.iteration_bunch(100)
