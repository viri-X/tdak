import numpy as np
from scipy.stats import zscore
from persim import wasserstein

class ClusterAnalyzer:
    """
    Comprehensive topological analysis for Kubernetes failure detection
    
    Features:
    - Wasserstein distance comparisons
    - Persistence entropy calculations
    - Storage outlier detection
    - Failure signature matching
    - Multi-scale topological change analysis
    """
    
    # Failure signature database
    FAILURE_SIGNATURES = {
        "zone_outage": {
            "Metric H0": "Large component increase (Δ ≥ 2)",
            "Network H0": "Component fragmentation",
            "Key Indicator": "Wasserstein H0 > 1.5 + Entropy H0 ↓"
        },
        "storage_failure": {
            "Metric H0": "High entropy dispersion",
            "Network H0": "Stable components",
            "Key Indicator": "Storage outliers + Entropy H0 ↑"
        },
        "network_congestion": {
            "Network H1": "Persistent cycle formation",
            "Metric Space": "Stable persistence",
            "Key Indicator": "H1 cycles > 2 + Wasserstein H1 > 1.0"
        },
        "dns_failure": {
            "Network H0": "Dependency breakdown",
            "Network H1": "Cycle collapse",
            "Key Indicator": "Active dependencies ↓ 50% + Entropy H0 ↑"
        },
        "pod_overload": {
            "Metric H1": "Resource contention patterns",
            "Network H0": "Stable services",
            "Key Indicator": "Wasserstein H1 > 0.8 + CPU/Memory correlation"
        }
    }

    '''def analyze(self, normal_metric, failed_metric, normal_network, failed_network, failure_type):
        """
        Complete topological analysis pipeline
        
        Args:
            normal_metric: Pre-failure metric persistence diagrams
            failed_metric: Post-failure metric persistence diagrams
            normal_network: Pre-failure network persistence diagrams
            failed_network: Post-failure network persistence diagrams
            failure_type: Type of simulated failure
            
        Returns:
            Dictionary with full analysis results
        """
        return {
            "failure_type": failure_type,
            "metric": self._analyze_metric_space(normal_metric, failed_metric),
            "network": self._analyze_network_complex(normal_network, failed_network),
            "storage_outliers": self._detect_storage_outliers(failed_metric),
            "signature_match": self.FAILURE_SIGNATURES.get(failure_type, {})
        }'''



    def analyze(self, normal_metric, failed_metric, normal_network, failed_network, failure_type, failed_nodes):
        """Updated to accept failed_nodes parameter"""
        return {
            "failure_type": failure_type,
            "metric": self._analyze_metric_space(normal_metric, failed_metric, failed_nodes),
            "network": self._analyze_network_complex(normal_network, failed_network),
            "storage_outliers": self._detect_storage_outliers(failed_nodes),
            "signature_match": self.FAILURE_SIGNATURES.get(failure_type, {})
        }

    def _analyze_metric_space(self, before, after, nodes):
        """Multi-dimensional resource metric analysis"""
        return {
            "h0": self._dimension_analysis(before, after, 0),
            "h1": self._dimension_analysis(before, after, 1),
            "storage_stats": self._storage_statistics(nodes)  # Pass actual node list"
            #storage_stats": self._storage_statistics(after)
        }

    def _analyze_network_complex(self, before, after):
        """Service dependency network analysis"""
        return {
            "h0": self._dimension_analysis(before, after, 0),
            "h1": self._dimension_analysis(before, after, 1),
            "active_dependencies": self._count_active_dependencies(after)
        }

    def _dimension_analysis(self, before_dgms, after_dgms, dim):
        """Analyze specific persistence diagram dimension"""
        before = self._safe_get_dimension(before_dgms, dim)
        after = self._safe_get_dimension(after_dgms, dim)
        
        return {
            "wasserstein": wasserstein(before, after) if len(before) and len(after) else 0,
            "component_diff": len(after) - len(before),
            "entropy_diff": self._persistence_entropy(after, dim) - self._persistence_entropy(before, dim)
        }

    '''def _detect_storage_outliers(self, metric_dgms):
        """Identify nodes with abnormal storage usage"""
        if len(metric_dgms) == 0 or len(metric_dgms[0]) == 0:
            return 0
            
        storage_values = [point[3] for point in metric_dgms[0]]  # 4th feature is storage
        return sum(np.abs(zscore(storage_values)) > 2.5)'''

    def _detect_storage_outliers(self, nodes):
        """Use actual node storage data"""
        if not nodes:
            return 0
        storage_values = [n.storage_usage for n in nodes]
        return sum(np.abs(zscore(storage_values)) > 2.5)

    '''def _persistence_entropy(self, dgms, dim):
        """Calculate normalized entropy for persistence diagram dimension"""
        if len(dgms) <= dim or len(dgms[dim]) == 0:
            return 0.0
            
        lifetimes = dgms[dim][:, 1] - dgms[dim][:, 0]
        lifetimes = lifetimes[lifetimes > 1e-9]  # Filter numerical zeros
        
        if len(lifetimes) == 0:
            return 0.0
            
        probabilities = lifetimes / lifetimes.sum()
        return -np.sum(probabilities * np.log(probabilities + 1e-9))'''

    def _persistence_entropy(self, dgms, dim):
        """Calculate normalized entropy for persistence diagram dimension"""
        # Validate diagram structure first
        if len(dgms) <= dim or dgms[dim].ndim != 2 or dgms[dim].shape[1] != 2:
            return 0.0
    
        diagram = dgms[dim]
        if diagram.size == 0:
            return 0.0
        
        lifetimes = diagram[:, 1] - diagram[:, 0]
        lifetimes = lifetimes[lifetimes > 1e-9]  # Filter numerical zeros
    
        if len(lifetimes) == 0:
            return 0.0
        
        probabilities = lifetimes / lifetimes.sum()
        return -np.sum(probabilities * np.log(probabilities + 1e-9))

    '''def _safe_get_dimension(self, dgms, dim):
        """Safely extract dimension data with validation"""
        if len(dgms) > dim and dgms[dim].ndim == 2:
            return dgms[dim]
        return np.empty((0, 2))'''

    def _safe_get_dimension(self, dgms, dim):
        """Returns guaranteed 2D array for specified dimension"""
        if len(dgms) > dim and isinstance(dgms[dim], np.ndarray) and dgms[dim].ndim == 2:
            return dgms[dim]
        return np.empty((0, 2))  # Empty but properly dimensioned


    '''def _storage_statistics(self, metric_dgms):
        """Calculate storage usage statistics"""
        if len(metric_dgms) == 0 or len(metric_dgms[0]) == 0:
            return {}
            
        storage_values = [point[3] for point in metric_dgms[0]]
        return {
            "mean": np.mean(storage_values),
            "max": np.max(storage_values),
            "outliers": sum(np.abs(zscore(storage_values)) > 2.5)
        }'''

    def _storage_statistics(self, nodes):
        """Calculate storage stats from nodes"""
        if not nodes:
            return {}
        storage_values = [n.storage_usage for n in nodes]
        return {
            "mean": np.mean(storage_values),
            "max": np.max(storage_values),
            "outliers": sum(np.abs(zscore(storage_values)) > 2.5)
        }

    def _count_active_dependencies(self, network_dgms):
        """Count active service dependencies from network diagram"""
        if len(network_dgms) == 0 or len(network_dgms[0]) == 0:
            return 0
        return len(network_dgms[0])  # H0 components ≈ active dependencies
    
    def validate_signature(self, report, failure_type):
        """Simplified signature validation for testing"""
        if failure_type == "zone_outage":
            return (
                report['network']['h0']['component_diff'] >= 2
                and report['metric']['h0']['wasserstein'] > 1.0
            )
        return False
