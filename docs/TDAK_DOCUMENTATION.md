# TDAK Documentation

:construction: This documentation is currently under construction. Consider it a placeholder for now.

## Table of Contents
1. [Theoretical Foundations](#1-theoretical-foundations)  
2. [Installation Guide](#2-installation-guide)  
3. [CLI Reference](#3-cli-reference)  
4. [API Documentation](#4-api-documentation)  
5. [Failure Type Catalog](#5-failure-type-catalog)  
6. [Advanced Configuration](#6-advanced-configuration)  

## 1. Theoretical Foundations
### Persistent Homology in K8s
Explanation of how topological features correspond to network states...

```python
# Example: Tracking H1 cycles
diagrams = analyzer.compute_network_persistence(dependencies)
```

### The Kubernetes Network:
**Mathematical definition:**
At this stage of the project, the code moke a set of relevant features of the kubernetes network for the analysis to be done. In a future, the code will lift this relevant features of actual kubernetes networks to monitor and predict possible faiulures. It is important to notice that, moked or real, this set of relevant features are modeled as a mathematical abstraction that we will call "the network model",  or "the network " or "the kubernetes network" in an abuse of language. So, lets clarify whats our network model is for TDAK, up to now, and what is implemented in the code.

-1. **Formal Network Model Definition**
In our model, the network is a set of interconnected devices (nodes) that communicate via shared protocols. Mathematically, it’s a directed graph 
$𝐺 = (𝑉, 𝐸)$, where: 
 - $V$: Nodes (e.g., servers, routers, pods).
 - $E$: Edges (e.g., physical cables, wireless links, virtual connections).
-----------------------------------------------------------------------------------------------

-2. **Core Networking Layers (OSI Model)**
Networks are structured into abstraction layers.

**Layer 3 (Network Layer)**
 - **Function:** Routes data between nodes using IP addresses.

 - **IP Address:** A unique identifier for a node (e.g., 192.168.1.2).

  - Analogous to coordinates in a graph $G$.

 - **Subnet:** A subset of IP addresses (e.g., 192.168.1.0/24).

**Layer 4 (Transport Layer)**
 - **Function:** Manages end-to-end communication (reliability, ports).

 - **TCP:** Connection-oriented protocol (like a handshake-proof function).

 - **UDP:** Connectionless protocol (like broadcasting a value).

**Layer 7 (Application Layer)**
 - **Function:** User-facing protocols (HTTP, DNS).

 - **DNS:** Maps domain names (e.g., google.com) to IP addresses (like a hash function).



## 2. Installation Guide
### Kubernetes Integration
```bash
helm install tdak ./charts --set zones=5
```

## 3. CLI Reference
### Command Structure
```bash
tdak-demo [FAILURE_TYPE] [--zones NUM] [--output FORMAT]
```

| Argument       | Description                              | Default |
|----------------|------------------------------------------|---------|
| `--zones`      | Number of availability zones            | 3       |
| `--threshold`  | Persistence threshold for filtering     | 0.15    |

## 4. API Documentation
### Core Classes
```python
class ClusterGenerator:
    """Simulates Kubernetes cluster states with failure injection"""
    
    def inject_failure(self, nodes, failure_type):
        """Apply specified failure pattern to cluster"""
```

## 5. Failure Type Catalog
| Failure        | Topological Signature           | Detection Metrics       |
|----------------|----------------------------------|-------------------------|
| Zone Outage    | H0 network components ↑↑        | Wasserstein > 1.5       |
| DNS Failure    | H1 cycles ↓↓                    | Entropy Δ > 0.4         |

## 6. Advanced Configuration
### Custom Metrics
```yaml
# config.yaml
metrics:
  - name: custom_metric
    weights: [0.3, 0.7]
    thresholds:
      H0: 0.45
```


