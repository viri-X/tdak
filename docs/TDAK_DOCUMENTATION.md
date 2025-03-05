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



##Older TDAK DOCUMENTATION




# TDAK: Topological Detection of Anomalies in Kubernetes

## 1. Data Flow Overview

```mermaid
graph TD
    A[Cluster Simulation] --> B[Generate Normal State]
    B --> C[Compute Metric Persistence]
    B --> D[Compute Network Persistence]
    C --> E[Topological Analysis]
    D --> E
    A --> F[Inject Failure]
    F --> G[Compute Failed Metric Persistence]
    F --> H[Compute Failed Network Persistence]
    G --> I[Comparative Analysis]
    H --> I
    I --> J[Visualization & Reporting]



# TDAK: Topological Kubernetes Failure Detection

## 1. Data Flow Overview

### 1.1 Data Generation Flow

**network.py**: Simulates Kubernetes cluster state through:  
- Node resource metrics (CPU, Memory, Storage, Pods)  
- Service dependency network (Ingress relationships)  

**topology.py**: Constructs topological spaces from:  
- Point cloud of node metrics (Metric Persistence)  
- Network connectivity graph (Network Persistence)  

**analysis.py**: Compares persistence diagrams using:  
- Wasserstein distances (Topological similarity)  
- Persistence entropy (Complexity measurement)  
- Betti number changes (Component/Cycle counting)  

## 2. Component Breakdown

### 2.1 Core Modules

**network.py**  
`Node`: Represents Kubernetes node with:  
- Resource metrics (CPU/Memory/Storage/Pod load)  
- Critical services (Ingress controllers)  
- Health status indicators  

`ClusterGenerator`: Creates synthetic clusters with:  
- Zone-aware node distribution  
- Service dependency injection  
- Failure simulation mechanisms  

**topology.py**  
`TopologyAnalyzer`: Computes persistence diagrams using:  
- Metric space analysis (Rips complex on node metrics)  
- Network analysis (Graph distance matrix)  
- Finite point filtering for stability  

**analysis.py**  
`ClusterAnalyzer`: Detects failures through:  
- Topological signature matching  
- Multi-scale metric comparisons  
- Storage outlier detection  

## 3. Failure-Topology Relationship Analysis

### 3.1 Zone Outage (AZ Failure)
**Topological Impact**:  
- **Metric Space**:  
  - H0: ↓ Connected components (Nodes removed)  
  - Entropy: ↓ (Simpler structure)  
  - Wasserstein: ↑ (Large metric space deformation)  
- **Network**:  
  - H0: ↑ Components (Network fragmentation)  
  - H1: ↓ Cycles (Broken service loops)  
  - Signature: Component explosion with cycle collapse  

**Why It Works**: Zone removal creates "holes" in both metric distribution and service network. The simultaneous H0 increase in network space and decrease in metric space provides unique signature.

### 3.2 Storage Failure
**Topological Impact**:  
- **Metric Space**:  
  - H1: ↑ 1D holes (Resource contention patterns)  
  - Entropy: ↑ (Irregular metric distribution)  
  - Outliers: ↑ (Storage usage spikes)  
- **Network**:  
  - Minimal change (Services remain connected)  
  - Signature: High metric entropy with stable network  

**Why It Works**: Localized storage failures create "spikes" in the metric space while leaving service dependencies intact. Persistence entropy detects abnormal metric distributions.

### 3.3 Network Congestion
**Topological Impact**:  
- **Network**:  
  - H1: ↑ Persistent cycles (Latency-induced loops)  
  - Wasserstein H1: ↑ (Cycle strength changes)  
  - Entropy: ↑ (Irregular latency distribution)  
- **Metric Space**:  
  - Stable topology  
  - Signature: Cycle proliferation without resource changes  

**Why It Works**: Increased latency modifies effective network distances, creating persistent cycles visible in H1 diagrams. Wasserstein distance detects cycle strength changes.

### 3.4 DNS Failure
**Topological Impact**:  
- **Network**:  
  - H0: ↑↑ Connected components (Service isolation)  
  - H1: ↓↓ Cycles (Dependency breakdown)  
  - Entropy: ↓ (Simpler network structure)  
- **Metric Space**:  
  - Stable topology  
  - Signature: Network fragmentation signature  

**Why It Works**: Disabled dependencies fragment the service network into disconnected components while eliminating cycles.

### 3.5 Pod Overload
**Topological Impact**:  
- **Metric Space**:  
  - H1: ↑ Resource contention patterns  
  - Wasserstein: ↑ (Metric space stretching)  
  - Entropy: ↑ (Complex resource relationships)  
- **Network**:  
  - Stable topology  
  - Signature: Metric space complexity with stable services  

**Why It Works**: Correlated CPU/Memory/Pod metrics create higher-dimensional topological features detectable through H1 analysis.

## 4. Topological Signature Table

| Failure Type       | Metric H0 | Metric H1 | Network H0 | Network H1 | Key Indicators                     |
|--------------------|-----------|-----------|------------|------------|------------------------------------|
| Zone Outage        | ↓↓        | –         | ↑↑         | ↓↓         | Component inverse correlation      |
| Storage Failure    | –         | ↑         | –          | –          | High metric entropy + outliers     |
| Network Congestion | –         | –         | –          | ↑↑         | Cycle proliferation                |
| DNS Failure        | –         | –         | ↑↑         | ↓↓         | Network fragmentation              |
| Pod Overload       | –         | ↑↑        | –          | –          | Metric space complexity            |

## 5. Why Topology Works for K8s Failures

- **Holistic View**: Captures both resource metrics *and* service relationships  
- **Noise Resistance**: Persistent homology filters transient fluctuations  
- **Early Detection**: Topological changes precede threshold breaches  
- **Failure Isolation**: Unique signatures enable precise diagnosis  
- **Non-Linear Relationships**: Detects complex resource interactions



## 6. Running the Demo

### 6.1 Command Line Interface
```bash
python demo.py <failure_type> [--zones NUM_ZONES]
```
Arguments:

Parameter	Description	Default	Required
failure_type	Type of failure to simulate	-	Yes
--zones	Number of availability zones in cluster	3	No
Supported Failure Types:

zone_outage: Simulates complete failure of an availability zone

storage_failure: Induces storage subsystem failures

network_congestion: Creates artificial network latency

dns_failure: Breaks service DNS resolution

pod_overload: Simulates pod resource exhaustion



Example:

```bash

# Simulate network congestion in 5-zone cluster
python demo.py network_congestion --zones 5
```

6.2 ASCII Logo Explanation
The TDAK logo in the help text is ASCII art spelling "TDAK":
```ASCII

████████╗██████╗  █████╗ ██╗  ██╗
╚══██╔══╝██╔══██╗██╔══██╗██║ ██╔╝
   ██║   ██████╔╝███████║█████╔╝ 
   ██║   ██╔══██╗██╔══██║██╔═██╗ 
   ██║   ██║  ██║██║  ██║██║  ██╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
``
The apparent "R" is part of the block character styling of the "D". This is intentional ASCII art formatting, not a typo.

6.3 Output Interpretation
Metric Persistence Diagram (Left):

X-axis: Birth time of topological features

Y-axis: Death time of features

Points far from diagonal = persistent features

Network Persistence Diagram (Right):

Triangles represent 1D cycles (H1)

Position indicates connection strength/latency

Empty diagram = no active dependencies

Signature Matching:

Compare reported Wasserstein distances and entropy changes against known failure patterns in the documentation