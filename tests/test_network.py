# Test
from datetime import datetime
from tdak.network import Node

def test_node_creation():
    # Create node with all required fields
    node = Node(
        name="node1",
        zone="zone-a",
        cpu_load=0.5,
        memory_usage=0.3,
        running_pods=2,
        storage_usage=0.4,
        critical_services=["ingress"],
        last_heartbeat=datetime.now()
    )
    
    assert node.name == "node1"
    assert node.zone == "zone-a"
    assert node.cpu_load == 0.5
    assert node.dns_healthy  # Should default to True

    
