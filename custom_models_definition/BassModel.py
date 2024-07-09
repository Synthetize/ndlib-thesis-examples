import future.utils
import numpy as np
import networkx as nx
from ndlib.models.DiffusionModel import DiffusionModel


class BassModel(DiffusionModel):

    def __init__(self, graph):
        #Call super class constructor
        super(self.__class__, self).__init__(graph)

        #Model name
        self.name = "Bass Model"

        #Available node statuses
        self.available_statuses = {
            "Non-Adopter": 0,
            "Infected": 1
        }

        #Exposed parameters
        self.parameters = {
            "model": {
                "p": {
                    "descr": "Innovation coefficient",
                    "range": [0, 1],
                    "optional": False
                },
                "q": {
                    "descr": "Imitation coefficient",
                    "range": [0, 1],
                    "optional": False
                }
            },
            "nodes": {},
            "edges": {}
        }

    def get_adoption_rate(self, t):
        p = self.params['model']['p']
        q = self.params['model']['q']
        total_nodes = self.graph.number_of_nodes()
        return p * q * total_nodes - (p * q) ** 2 * t

    def get_adopted_fraction(self):
        adopter_count = 0
        for n in self.status:
            if self.status[n] == 1:
                adopter_count += 1
        return adopter_count / self.graph.number_of_nodes()

    def iteration(self, node_status=True):
        self.clean_initial_status(self.available_statuses.values())
        actual_status = {node: nstatus for node, nstatus in self.status.items()}

        # if first iteration return the initial node status
        if self.actual_iteration == 0:
            self.actual_iteration += 1
            delta, node_count, status_delta = self.status_delta(actual_status)
            if node_status:
                return {"iteration": 0, "status": actual_status.copy(),
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
            else:
                return {"iteration": 0, "status": {},
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}

        # iteration inner loop
        for u in self.graph.nodes():
            if actual_status[u] == 0:
                # non-adopter
                # evaluate the adoption rate
                print("Iteration: ", self.actual_iteration)
                adopt_rate = self.get_adoption_rate(self.actual_iteration)
                adopter_rate = self.get_adopted_fraction()
                print(f"Adopt rate: {adopt_rate}, Adopter rate: {adopter_rate}")
                individual_rate = adopt_rate * adopter_rate
                if np.random.random() < individual_rate:
                    # adopt the innovation
                    actual_status[u] = 1

        # identify the changes w.r.t. previous iteration
        delta, node_count, status_delta = self.status_delta(actual_status)

        # update the actual status and iterative step
        self.status = actual_status
        self.actual_iteration += 1

        # return the actual configuration (only nodes with status updates)
        if node_status:
            return {"iteration": self.actual_iteration - 1, "status": delta.copy(),
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
        else:
            return {"iteration": self.actual_iteration - 1, "status": {},
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
