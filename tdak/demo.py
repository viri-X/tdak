import argparse
import matplotlib.pyplot as plt
from persim import plot_diagrams
from tdak.network import ClusterGenerator
from tdak.topology import TopologyAnalyzer
from tdak.analysis import ClusterAnalyzer

def main():
    parser = argparse.ArgumentParser(
        description='''

        ████████╗██████╗  █████╗ ██╗  ██╗
        ╚══██╔══╝██╔══██╗██╔══██╗██║ ██╔╝
           ██║   ██║  ██║███████║█████╔╝ 
           ██║   ██║  ██║██╔══██║██╔═██╗ 
           ██║   ██████╔╝██║  ██║██║  ██╗
           ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
        Topological Kubernetes Failure Detection
        ''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('failure', choices=[
        'zone_outage', 'storage_failure', 
        'network_congestion', 'dns_failure', 
        'pod_overload'
    ], help='Failure type to simulate')
    parser.add_argument('--zones', type=int, default=3,
                       help='Number of availability zones')
    args = parser.parse_args()

    # Initialize components
    gen = ClusterGenerator(args.zones)
    topo = TopologyAnalyzer()
    analyzer = ClusterAnalyzer()
    
    # Generate cluster state
    nodes = gen.generate_cluster()
    print(f"\n 🌐 Generated cluster with {len(nodes)} nodes across {args.zones} zones")
    
    # Compute initial topologies
    metric_initial = topo.compute_metric_persistence(nodes)
    network_initial = topo.compute_network_persistence(gen.service_deps)
    
    # Inject failure and compute new state
    failed_nodes = gen.inject_failure(nodes, args.failure)
    metric_failed = topo.compute_metric_persistence(failed_nodes)
    network_failed = topo.compute_network_persistence(gen.service_deps)
    
    # Perform comprehensive analysis
    report = analyzer.analyze(
        metric_initial, metric_failed,
        network_initial, network_failed,
        args.failure,
        failed_nodes  # parameter added
    )
    
    # Generate report
    print(f"\n🔍 {' FAILURE ANALYSIS REPORT ':=^80}")
    print(f"\n🚨 Failure Type: {args.failure.upper()}")
    
    # Metric space findings
    print(f"\n📊 {' METRIC SPACE ANALYSIS ':-^80}")
    print(f"  H0 Components: {len(metric_initial[0])} → {len(metric_failed[0])} "
          f"(Δ{report['metric']['h0']['component_diff']})")
    print(f"  Wasserstein Distance H0: {report['metric']['h0']['wasserstein']:.2f}")
    print(f"  Entropy Change H0: {report['metric']['h0']['entropy_diff']:+.2f}")
    print(f"  Storage Outliers: {report['storage_outliers']}")
    
    # Network findings
    print(f"\n🕸️ {' NETWORK ANALYSIS ':-^80}")
    print(f"  Active Dependencies: {len([sd for sd in gen.service_deps if sd.active])}/{len(gen.service_deps)}")
    print(f"  H1 Cycles: {len(network_failed[1]) if len(network_failed)>1 else 0} "
          f"(Δ{report['network']['h1']['component_diff']})")
    print(f"  Wasserstein Distance H1: {report['network']['h1']['wasserstein']:.2f}")
    print(f"  Entropy Change H1: {report['network']['h1']['entropy_diff']:+.2f}")
    
    # Signature matching
    print(f"\n🔎 {' SIGNATURE MATCHING ':-^80}")
    for feature, description in report['signature_match'].items():
        print(f"  ✔️ {feature}: {description}")
    
    # Visualization
    plt.figure(figsize=(15, 6))

    # Metric diagram plot
    plt.subplot(121, title="Resource Metric Persistence")
    plot_diagrams(metric_failed)

    # Network diagram plot (handle empty case)
    plt.subplot(122, title="Network Connectivity Persistence")
    if any(len(d) > 0 for d in network_failed):
        plot_diagrams(network_failed)
    else:
        plt.text(0.5, 0.5, 'No Network Dependencies', 
                 ha='center', va='center', fontsize=12)
        plt.xlim(0, 1)
        plt.ylim(0, 1)

    plt.tight_layout()
    #plt.savefig(f"{failure_type}_analysis.png", dpi=150)
    #print(f"\n📈 Visualization saved to {failure_type}_analysis.png")
    plt.show() # Pop up interactive matplotlib window
    
if __name__ == "__main__":
    main()
    
    
