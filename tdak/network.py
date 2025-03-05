import numpy as np
from dataclasses import dataclass, replace
from datetime import datetime
from typing import List
import random

@dataclass
class Node:
    name: str
    zone: str
    cpu_load: float
    memory_usage: float
    running_pods: int
    storage_usage: float
    critical_services: List[str]
    last_heartbeat: datetime
    dns_healthy: bool = True

@dataclass
class ServiceDependency:
    source: str
    target: str
    latency_ms: float
    active: bool = True

class ClusterGenerator:
    def __init__(self, num_zones=3):
        self.zones = [f"zone-{i}" for i in range(num_zones)]
        self.node_counter = 0
        self.service_deps = []
        
    def generate_cluster(self):
        nodes = []
        for zone in self.zones:
            for _ in range(np.random.randint(2, 5)):
                nodes.append(self._create_node(zone))
        self._create_dependencies(nodes)
        return nodes
    
    def _create_node(self, zone):
        self.node_counter += 1
        return Node(
            name=f"{zone}-node-{self.node_counter}",
            zone=zone,
            cpu_load=np.clip(np.random.beta(2, 5), 0, 1),
            memory_usage=np.clip(np.random.beta(2, 5), 0, 1),
            running_pods=np.random.poisson(3),
            storage_usage=np.clip(np.random.beta(1, 3), 0, 1),
            critical_services=["ingress"] if np.random.rand() < 0.2 else [],
            last_heartbeat=datetime.now()
        )

    def _create_dependencies(self, nodes):
        self.service_deps = []
        svc_nodes = [n for n in nodes if "ingress" in n.critical_services]
        for src in svc_nodes:
            tgt_candidates = [n for n in svc_nodes if n != src]
            if len(tgt_candidates) >= 2:
                for tgt in random.sample(tgt_candidates, 2):
                    self.service_deps.append(ServiceDependency(
                        src.name, tgt.name,
                        latency_ms=10 if src.zone == tgt.zone else 150
                    ))

    def inject_failure(self, nodes, failure_type):
        if failure_type == "zone_outage":
            return self._zone_outage(nodes)
        elif failure_type == "storage_failure":
            return self._storage_failure(nodes)
        elif failure_type == "network_congestion":
            return self._network_congestion(nodes)
        elif failure_type == "dns_failure":
            return self._dns_failure(nodes)
        elif failure_type == "pod_overload":
            return self._pod_overload(nodes)
        return nodes

    def _zone_outage(self, nodes):
        dead_zone = np.random.choice(self.zones)
        dead_nodes = {n.name for n in nodes if n.zone == dead_zone}
        self.service_deps = [
            sd for sd in self.service_deps
            if sd.source not in dead_nodes and sd.target not in dead_nodes
        ]
        return [n for n in nodes if n.zone != dead_zone]

    def _storage_failure(self, nodes):
        return [
            replace(n, storage_usage=1.0) 
            if random.random() < 0.25 else n
            for n in nodes
        ]

    def _network_congestion(self, nodes):
        for sd in self.service_deps:
            if random.random() < 0.3:
                sd.latency_ms *= 10
        return nodes

    def _dns_failure(self, nodes):
        # Disable 50% of dependencies
        for sd in random.sample(self.service_deps, k=int(len(self.service_deps)*0.5)):
            sd.active = False
        
        # Mark 30% nodes with DNS issues
        return [
            replace(n, dns_healthy=False)
            if random.random() < 0.3 else n
            for n in nodes
        ]

    def _pod_overload(self, nodes):
        return [
            replace(n,
                cpu_load=min(n.cpu_load * 1.8, 1.0),
                memory_usage=min(n.memory_usage * 1.5, 1.0),
                running_pods=n.running_pods + 5
            ) for n in nodes
        ]

    # other failures ...
