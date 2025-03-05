#test_network
# tests/test_network.py
from datetime import datetime
import pytest
from tdak.network import Node, ServiceDependency

class TestNetworkComponents:
    def setup_method(self):
        # Common test data
        self.valid_node_args = {
            "name": "node1",
            "zone": "zone-a",
            "cpu_load": 0.5,
            "memory_usage": 0.3,
            "running_pods": 2,
            "storage_usage": 0.4,
            "critical_services": ["ingress"],
            "last_heartbeat": datetime.now()
        }
        
        self.valid_service_dep_args = {
            "source": "node1",
            "target": "node2",
            "latency_ms": 150,
            "active": True
        }

    def test_node_creation_with_defaults(self):
        """Verify Node initialization with default DNS health status"""
        node = Node(**self.valid_node_args)
        assert node.dns_healthy is True
        assert node.critical_services == ["ingress"]

    def test_node_creation_explicit_dns(self):
        """Test explicit DNS health flag"""
        node = Node(**self.valid_node_args, dns_healthy=False)
        assert node.dns_healthy is False

    @pytest.mark.parametrize("missing_field", [
        "name", "zone", "cpu_load", "memory_usage",
        "running_pods", "storage_usage", "critical_services",
        "last_heartbeat"
    ])
    def test_node_required_fields(self, missing_field):
        """Ensure required fields throw errors when missing"""
        args = self.valid_node_args.copy()
        del args[missing_field]
        
        with pytest.raises(TypeError):
            Node(**args)

    def test_service_dependency_creation(self):
        """Verify basic ServiceDependency initialization"""
        dep = ServiceDependency(**self.valid_service_dep_args)
        assert dep.source == "node1"
        assert dep.target == "node2"
        assert dep.latency_ms == 150
        assert dep.active is True

    def test_service_dependency_default_active(self):
        """Test default active status when not provided"""
        args = self.valid_service_dep_args.copy()
        del args["active"]
        dep = ServiceDependency(**args)
        assert dep.active is True  # From ServiceDependency definition

    def test_service_dependency_latency_validation(self):
        """Ensure latency cannot be negative"""
        with pytest.raises(ValueError):
            ServiceDependency(**{**self.valid_service_dep_args, "latency_ms": -50})

    def test_inactive_dependency(self):
        """Verify inactive dependencies are tracked correctly"""
        dep = ServiceDependency(**{**self.valid_service_dep_args, "active": False})
        assert dep.active is False