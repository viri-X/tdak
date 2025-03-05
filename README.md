# TDAK - Topological Kubernetes Failure Detection
[![CI Tests](https://github.com/viri-X/tdak/actions/workflows/tests.yml/badge.svg)](https://github.com/viri-X/tdak/actions)

**Detect anomalies in Kubernetes networks using persistent homology and topological data analysis**.

## Key Features
- 🌀 Real-time topological analysis of cluster states
- 🔧 5+ preconfigured failure scenarios
- 📊 Interactive persistence diagram visualization
- 📈 Resource metric tracking with Wasserstein distances

## Quick Start

## Installation

```bash
pip install git+https://github.com/viri-X/tdak.git
```

## 🚀 Basic Usage

Run anomaly detection demos with:

```bash
tdak-demo dns_failure --zones 5
```
Supported Failure Types:

zone_outage: Simulate availability zone failure

storage_failure: Induce storage system degradation

network_congestion: Create artificial latency spikes

dns_failure: Break service DNS resolution

pod_overload: Simulate resource exhaustion


Example:

```bash
# Simulate DNS failure in 5-zone cluster
tdak-demo dns_failure --zones 15
```

For full options:

```bash
tdak-dem --help
```


## Documentation Hub
- [Technical Architecture](docs/ARCHITECTURE.md)  
- [Full Documentation](docs/TDAK_DOCUMENTATION.md)  
- [API Reference](docs/API_REFERENCE.md) (WIP)

## Contributing
```bash
git clone https://github.com/viri-X/tdak.git
pip install -e .[dev]
pytest tests/
```


## Enhanced Failure Modes

| Failure Type          | Simulation Method                             | Topological Signature                     |
|-----------------------|-----------------------------------------------|-------------------------------------------|
| Zone Outage           | Remove all nodes from random zone             | Increased H0 components                   |
| Pod Overload          | Spike CPU/memory + add pods                   | Compressed metric space                   |
| Network Congestion    | 30% connections ×10 latency                   | Elongated 1-cycles                        |
| DNS Failures          | Disable 50% dependencies                      | Broken edges in network complex           |
| Storage Failures      | Max storage on 25% nodes                      | Metric space outliers                     |

