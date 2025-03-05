# tests/test_topology.py
import numpy as np
from datetime import datetime
from tdak.network import ServiceDependency
from tdak.topology import TopologyAnalyzer
from tdak.network import Node

class TestTopologyAnalyzer:
    def setup_method(self):
        self.analyzer = TopologyAnalyzer()
        
        # Sample service dependencies
        self.deps = [
            ServiceDependency("node1", "node2", 50, True),
            ServiceDependency("node2", "node3", 150, False)
        ]

    def test_compute_metric_persistence_shape(self):
        """Verify metric persistence diagram structure"""
        nodes = [
            self._create_node("node1", 0.3, 0.4),
            self._create_node("node2", 0.6, 0.2)
        ]
        
        diagrams = self.analyzer.compute_metric_persistence(nodes)
        assert len(diagrams) == 3, "Expected H0, H1, H2 diagrams"
        assert diagrams[0].shape[1] == 2, "Birth/death pairs"

    def test_network_persistence_components(self):
        """Test connected components in service network"""
        diagrams = self.analyzer.compute_network_persistence(self.deps)
        # Active dependencies: node1 <-> node2 (active=True)
        assert len(diagrams[0]) == 1, "One connected component"

    def test_empty_network_persistence(self):
        """Handle empty dependency list"""
        diagrams = self.analyzer.compute_network_persistence([])
        assert len(diagrams[0]) == 0, "No nodes, no components"

    '''def _create_node(self, name, cpu_load, memory_usage):
        """Helper to create node objects"""
        return {
            "name": name,
            "test-zone": zone,
            "cpu_load": cpu_load,
            "memory_usage": memory_usage,
            "running_pods": 2,
            "storage_usage": 0.5,
            "critical_services": ["ingress"],
            "last_heartbeat": datetime.now()
        }'''
    
    def _create_node(self, name, cpu_load, memory_usage):
        """Helper to create node objects"""
        return Node(
            name=name,
            zone="test-zone",  # Fixed parameter name and added default value
            cpu_load=cpu_load,
            memory_usage=memory_usage,
            running_pods=2,
            storage_usage=0.5,
            critical_services=["ingress"],
            last_heartbeat=datetime.now()
        )