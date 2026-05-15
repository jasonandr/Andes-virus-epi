import matplotlib.pyplot as plt
import networkx as nx
import os
import time

def create_homogenous_network(n_nodes=20):
    G = nx.DiGraph()
    G.add_node(0, layer=0)
    
    current_node = 0
    next_node = 1
    
    # Create a long chain with a few tiny branches
    while next_node < n_nodes:
        # Homogenous: mostly 1 child, sometimes 0 or 2
        import random
        random.seed(next_node)
        children_count = random.choices([0, 1, 2], weights=[0.2, 0.7, 0.1])[0]
        
        # Force at least some progress to use up nodes
        if children_count == 0 and next_node < n_nodes - 2:
            children_count = 1
            
        for _ in range(children_count):
            if next_node < n_nodes:
                G.add_node(next_node, layer=G.nodes[current_node]['layer'] + 1)
                G.add_edge(current_node, next_node)
                next_node += 1
        current_node += 1
        if current_node >= next_node:
            # If line dies, start a new spark from 0 just to keep graph connected for visualization
            G.add_node(next_node, layer=1)
            G.add_edge(0, next_node)
            next_node += 1

    return G

def create_superspreader_network(n_nodes=20):
    G = nx.DiGraph()
    G.add_node(0, layer=0)
    
    # Index case infects massive amount (the hub)
    hub_children = 16
    for i in range(1, hub_children + 1):
        G.add_node(i, layer=1)
        G.add_edge(0, i)
        
    # One of the children is a minor superspreader
    for i in range(hub_children + 1, n_nodes):
        G.add_node(i, layer=2)
        G.add_edge(2, i) # node 2 infects the rest
        
    return G

def main():
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # 1. Homogenous
    G_homo = create_homogenous_network(22)
    pos_homo = nx.kamada_kawai_layout(G_homo)
    
    out_degrees = dict(G_homo.out_degree())
    node_colors_homo = ['darkred' if out_degrees[n] > 2 else 'steelblue' for n in G_homo.nodes()]
    node_sizes_homo = [800 if out_degrees[n] > 2 else 300 for n in G_homo.nodes()]
    
    nx.draw_networkx_nodes(G_homo, pos_homo, ax=axes[0], node_color=node_colors_homo, node_size=node_sizes_homo, edgecolors='white', linewidths=1.5)
    nx.draw_networkx_edges(G_homo, pos_homo, ax=axes[0], edge_color='gray', arrows=True, arrowsize=15, alpha=0.7)
    
    axes[0].set_title("Homogenous Spread (Poisson)\n" + r"$R_0 \approx 1.0, k \rightarrow \infty$", fontsize=16, fontweight='bold', pad=15)
    axes[0].axis('off')
    axes[0].text(0.5, -0.05, "Long, linear transmission chains.\nContact tracing focuses on individual links.", 
                 ha='center', va='center', transform=axes[0].transAxes, fontsize=13, style='italic')

    # 2. Superspreader
    G_super = create_superspreader_network(22)
    pos_super = nx.spring_layout(G_super, seed=42, k=0.5)
    
    out_degrees_super = dict(G_super.out_degree())
    node_colors_super = ['darkred' if out_degrees_super[n] > 2 else 'steelblue' for n in G_super.nodes()]
    node_sizes_super = [1500 if out_degrees_super[n] > 2 else 300 for n in G_super.nodes()]
    
    nx.draw_networkx_nodes(G_super, pos_super, ax=axes[1], node_color=node_colors_super, node_size=node_sizes_super, edgecolors='white', linewidths=2)
    nx.draw_networkx_edges(G_super, pos_super, ax=axes[1], edge_color='gray', arrows=True, arrowsize=15, alpha=0.7)
    
    axes[1].set_title("Superspreading Event (Negative Binomial)\n" + r"$R_0 \approx 1.0, k = 0.23$", fontsize=16, fontweight='bold', pad=15)
    axes[1].axis('off')
    axes[1].text(0.5, -0.05, "Massive 'Hub-and-Spoke' clusters.\nContact tracing must identify the central event.", 
                 ha='center', va='center', transform=axes[1].transAxes, fontsize=13, style='italic')
                 
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"network_plot_{timestamp}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved network plot to {plot_path}")

if __name__ == "__main__":
    main()
