import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import time
import re
import os
import matplotlib.dates as mdates

def main():
    data_path = "/Users/jasonandrews/repos/hanta/data/hondius_cases.csv"
    walkthrough_path = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts/walkthrough.md"
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    
    # Load data
    df = pd.read_csv(data_path)
    df['date_of_onset'] = pd.to_datetime(df['date_of_onset'])
    df['exposure_start'] = pd.to_datetime(df['exposure_start'])
    df['exposure_end'] = pd.to_datetime(df['exposure_end'])
    
    # ---------------------------------------------------------
    # 1. Transmission Network Graph
    # ---------------------------------------------------------
    G = nx.DiGraph()
    
    for idx, row in df.iterrows():
        G.add_node(row['case_id'], role=row['role'], status=row['status'], outcome=row['outcome'])
        if pd.notna(row['infector_id']) and row['infector_id'] != 'None':
            # ensure it's treated as float/int
            infector = int(float(row['infector_id']))
            G.add_edge(infector, row['case_id'])
            
    plt.figure(figsize=(10, 8))
    
    # Custom layout
    pos = nx.spring_layout(G, k=0.5, seed=42)
    
    # Node colors by role
    color_map = {'Passenger': '#3498db', 'Crew': '#e74c3c'}
    node_colors = [color_map[G.nodes[n]['role']] for n in G.nodes()]
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color=node_colors, edgecolors='white', linewidths=2)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray', connectionstyle='arc3,rad=0.1')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif', font_color='white', font_weight='bold')
    
    # Legend
    import matplotlib.lines as mlines
    passenger_patch = mlines.Line2D([], [], color='#3498db', marker='o', linestyle='None', markersize=10, label='Passenger')
    crew_patch = mlines.Line2D([], [], color='#e74c3c', marker='o', linestyle='None', markersize=10, label='Crew')
    plt.legend(handles=[passenger_patch, crew_patch], loc='upper right', title="Role")
    
    plt.title('MV Hondius Andes Virus Transmission Network', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    timestamp = int(time.time())
    network_plot_filename = f"network_plot_{timestamp}.png"
    network_plot_path = os.path.join(artifacts_dir, network_plot_filename)
    plt.savefig(network_plot_path, dpi=300)
    plt.close()
    print(f"Saved transmission network plot to {network_plot_path}")
    
    # ---------------------------------------------------------
    # 2. Exposure & Onset Gantt Chart
    # ---------------------------------------------------------
    plt.figure(figsize=(12, 6))
    
    # Plot exposure windows
    for idx, row in df.iterrows():
        # Plot exposure line
        plt.hlines(y=row['case_id'], xmin=row['exposure_start'], xmax=row['exposure_end'], 
                   color='lightgray', linewidth=5, zorder=1)
        
        # Plot onset point
        color = 'red' if row['outcome'] == 'Fatal' else 'green'
        marker = 'X' if row['outcome'] == 'Fatal' else 'o'
        plt.scatter(row['date_of_onset'], row['case_id'], color=color, s=100, zorder=2, marker=marker, edgecolor='black')
        
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.title('Patient Exposure Windows and Symptom Onset Timeline', fontsize=14, fontweight='bold')
    plt.xlabel('Date (2026)', fontsize=12)
    plt.ylabel('Patient Case ID', fontsize=12)
    plt.yticks(df['case_id'])
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Legend
    fatal_patch = mlines.Line2D([], [], color='red', marker='X', linestyle='None', markersize=10, label='Onset (Fatal)')
    recov_patch = mlines.Line2D([], [], color='green', marker='o', linestyle='None', markersize=10, label='Onset (Recovering)')
    exp_patch = mlines.Line2D([], [], color='lightgray', linewidth=5, label='Estimated Exposure Window')
    plt.legend(handles=[fatal_patch, recov_patch, exp_patch], loc='upper left')
    
    plt.tight_layout()
    gantt_plot_filename = f"gantt_plot_{timestamp}.png"
    gantt_plot_path = os.path.join(artifacts_dir, gantt_plot_filename)
    plt.savefig(gantt_plot_path, dpi=300)
    plt.close()
    print(f"Saved Gantt chart plot to {gantt_plot_path}")
    
    # ---------------------------------------------------------
    # Update Markdown Walkthrough
    # ---------------------------------------------------------
    with open(walkthrough_path, 'r') as f:
        md_content = f.read()
    
    # If the network plot or Gantt chart aren't in the markdown yet, we append them.
    if 'Transmission Network' not in md_content:
        new_md = "\n\n## Transmission Network\n"
        new_md += f"![Network Plot]({network_plot_path})\n"
        new_md += "\n## Exposure Timeline\n"
        new_md += f"![Gantt Chart]({gantt_plot_path})\n"
        md_content += new_md
    else:
        # Regex update if they exist
        md_content = re.sub(r'(!\[Network Plot\]\()[^\)]+(\))', rf'\g<1>{network_plot_path}\g<2>', md_content)
        md_content = re.sub(r'(!\[Gantt Chart\]\()[^\)]+(\))', rf'\g<1>{gantt_plot_path}\g<2>', md_content)
        
    with open(walkthrough_path, 'w') as f:
        f.write(md_content)
    print(f"Updated {walkthrough_path} with new plot references.")

if __name__ == "__main__":
    main()
