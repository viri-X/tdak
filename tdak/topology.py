# tdak/topology.py
import warnings
import numpy as np
from sklearn.preprocessing import StandardScaler
import ripser
from persim import wasserstein

class TopologyAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
    
    def compute_metric_persistence(self, nodes):
        """Compute persistence diagrams with finite death time filtering"""
        X = np.array([
            [n.cpu_load, n.memory_usage, 
             n.running_pods/10.0,
             n.storage_usage]
            for n in nodes
        ])

        # Preserve scaling while handling warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            scaled_X = self.scaler.fit_transform(X)
            dgms = ripser.ripser(scaled_X, maxdim=2)['dgms']
            
        return [self._filter_finite_points(d) for d in dgms]
    

    '''def compute_network_persistence(self, service_deps):
        """Network analysis with finite point filtering"""
        active_deps = [sd for sd in service_deps if sd.active]
        if not active_deps:
            return []
            
        nodes = sorted({sd.source for sd in active_deps} | {sd.target for sd in active_deps})
        size = len(nodes)
        adj_matrix = np.full((size, size), np.inf)
        np.fill_diagonal(adj_matrix, 0)
        node_idx = {n: i for i, n in enumerate(nodes)}
        
        for sd in active_deps:
            i, j = node_idx[sd.source], node_idx[sd.target]
            adj_matrix[i,j] = adj_matrix[j,i] = 1/(sd.latency_ms + 1e-9)
            
        raw_dgms = ripser.ripser(adj_matrix, distance_matrix=True, maxdim=2)['dgms']
        return [self._filter_finite_points(d) for d in raw_dgms]'''

    def compute_network_persistence(self, service_deps):
      """Network analysis with finite point filtering and empty state handling"""
      active_deps = [sd for sd in service_deps if sd.active]
    
      # Return properly structured empty diagrams when no dependencies
      if not active_deps:
          return [np.empty((0, 2)) for _ in range(3)]  # H0, H1, H2
    
      nodes = sorted({sd.source for sd in active_deps} | {sd.target for sd in active_deps})
      size = len(nodes)
      adj_matrix = np.full((size, size), np.inf)
      np.fill_diagonal(adj_matrix, 0)
      node_idx = {n: i for i, n in enumerate(nodes)}
    
      for sd in active_deps:
          i, j = node_idx[sd.source], node_idx[sd.target]
          adj_matrix[i,j] = adj_matrix[j,i] = 1/(sd.latency_ms + 1e-9)
        
      raw_dgms = ripser.ripser(adj_matrix, distance_matrix=True, maxdim=2)['dgms']
      return [self._filter_finite_points(d) for d in raw_dgms]

    '''def _filter_finite_points(self, diagram):
        """Remove points with non-finite death times"""
        if diagram.size == 0:
            return diagram
        return diagram[np.isfinite(diagram[:, 1])]'''

    def _filter_finite_points(self, diagram):
        """Returns properly shaped 2D array even when empty"""
        if diagram.ndim != 2 or diagram.shape[1] != 2:
            return np.empty((0, 2))  # Force 2D format
    
        finite_mask = np.isfinite(diagram[:, 1])
        filtered = diagram[finite_mask]
    
        # Maintain 2D shape even with single point
        return filtered.reshape(-1, 2) if filtered.size > 0 else np.empty((0, 2))

    def analyze_changes(self, dgms_before, dgms_after):
        """Robust diagram comparison with empty state handling"""
        analysis = {}
        for dim in [0, 1]:
            # Ensure we get 2D arrays even if empty
            before = self._ensure_2d_array(dgms_before, dim)
            after = self._ensure_2d_array(dgms_after, dim)
            
            analysis[f'h{dim}'] = {
                'wasserstein': wasserstein(before, after) if len(before) and len(after) else 0,
                'count_diff': after.shape[0] - before.shape[0],
                'entropy_diff': self.persistence_entropy(after, dim) - self.persistence_entropy(before, dim)
            }
        return analysis

    def _ensure_2d_array(self, dgms, dim):
        """Convert to empty 2D array if invalid"""
        if len(dgms) > dim and dgms[dim].ndim == 2:
            return dgms[dim]
        return np.empty((0, 2))

    def persistence_entropy(self, dgms, dim=0):
        """Entropy calculation with filtered diagrams"""
        diagram = self._ensure_2d_array(dgms, dim)
        
        if diagram.shape[0] == 0:
            return 0.0
            
        lifetimes = diagram[:, 1] - diagram[:, 0]
        lifetimes = lifetimes[lifetimes > 1e-9]
        
        if len(lifetimes) == 0:
            return 0.0
            
        probabilities = lifetimes / lifetimes.sum()
        return -np.sum(probabilities * np.log(probabilities + 1e-9))
    
    # extra topological tools ...
