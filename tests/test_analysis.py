# tests/test_analysis.py
from tdak.analysis import ClusterAnalyzer
from tdak.network import Node
import numpy as np

def test_analysis_signature_matching():
    analyzer = ClusterAnalyzer()
    dummy_report = {
        'metric': {'h0': {'wasserstein': 1.2}, 'h1': {'wasserstein': 0.8}},
        'network': {'h0': {'component_diff': 2}, 'h1': {'component_diff': -1}},
        'storage_outliers': 3,
        'signature_match': {}
    }
    
    result = analyzer.validate_signature(dummy_report, "zone_outage")
    assert isinstance(result, bool)