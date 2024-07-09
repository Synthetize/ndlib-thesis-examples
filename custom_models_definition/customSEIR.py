
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm
import numpy as np

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence

class CustomSEIRModel(gc.CompositeModel):
    def __init__(self, graph):
        super().__init__(graph)

        self.add_status("Susceptible")
        self.add_status("Exposed")
        self.add_status("Infected")
        self.add_status("Removed")

        config = mc.Configuration()
        config.add_model_parameter('beta', 0.05)  # Infection rate
        config.add_model_parameter('alpha', 0.01)  # Latent period (1/duration)
        config.add_model_parameter('gamma', 0.01)  # Recovery rate
        config.add_model_parameter('tp_rate', 1)  # Whether if the infection rate depends on the number of infected neighbors

        self.set_initial_status(config)
        c2 = cpm.NodeStochastic(0.05)
        self.add_rule("Exposed", "Infected", c2)

        c3 = cpm.NodeStochastic(0.01)
        self.add_rule("Infected", "Removed", c3)

    def iteration(self, node_status=True):
        # Qui puoi implementare la logica per calcolare la probabilità di infezione in base al numero di vicini infetti
        self.clean_initial_status(list(self.available_statuses.values()))

        actual_status = {node: nstatus for node, nstatus in future.utils.iteritems(self.status)}

        if self.actual_iteration == 0:
            self.actual_iteration += 1
            delta, node_count, status_delta = self.status_delta(actual_status)
            if node_status:
                return {"iteration": 0, "status": actual_status.copy(),
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
            else:
                return {"iteration": 0, "status": {},
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}

        for u in self.graph.nodes:

            u_status = self.status[u]
            eventp = np.random.random_sample()
            neighbors = self.graph.neighbors(u)
            if self.graph.directed:
                neighbors = self.graph.predecessors(u)

            if u_status == 0:  # Susceptible

                infected_neighbors = [v for v in neighbors if self.status[v] == 1]
                triggered = 1 if len(infected_neighbors) > 0 else 0

                if self.params['model']['tp_rate'] == 1:
                    if eventp < 1 - (1 - self.params['model']['beta']) ** len(infected_neighbors):
                        actual_status[u] = 2  # Exposed
                else:
                    if eventp < self.params['model']['beta'] * triggered:
                        actual_status[u] = 2  # Exposed

            for i in range(0, self.compartment_progressive):
                if u_status == self.available_statuses[self.compartment[i][0]]:
                    rule = self.compartment[i][2]
                    test = rule.execute(node=u, graph=self.graph, status=self.status,
                                        status_map=self.available_statuses, params=self.params)
                    if test:
                        actual_status[u] = self.available_statuses[self.compartment[i][1]]
                        break

        delta, node_count, status_delta = self.status_delta(actual_status)
        self.status = actual_status
        self.actual_iteration += 1

        if node_status:
            return {"iteration": self.actual_iteration - 1, "status": delta.copy(),
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
        else:
            return {"iteration": self.actual_iteration - 1, "status": {},
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}