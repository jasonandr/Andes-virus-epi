import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time

def simulate_outbreak(R0, k, max_generations=20, max_cases=500):
    current_cases = 1
    total_cases = 1
    
    for gen in range(max_generations):
        if current_cases == 0:
            break
            
        p = k / (k + R0)
        next_gen_cases = np.sum(np.random.negative_binomial(k, p, current_cases))
            
        current_cases = next_gen_cases
        total_cases += current_cases
        
        if total_cases >= max_cases:
            return max_cases
            
    return total_cases

def main():
    R0 = 0.96
    k = 0.23
    num_sims = 10000
    
    np.random.seed(42)
    nb_sizes = np.array([simulate_outbreak(R0, k) for _ in range(num_sims)])
    
    nb_ext_index = np.mean(nb_sizes == 1) * 100
    nb_major = np.mean(nb_sizes > 10) * 100
    
    plt.figure(figsize=(10, 6))
    
    # Raincloud plot components for log scale data
    # 1. KDE Plot (The "Cloud")
    ax = sns.kdeplot(x=nb_sizes, log_scale=True, fill=True, alpha=0.5, color='teal', linewidth=2, cut=0)
    
    # 2. Strip Plot (The "Rain")
    # Add some random y-jitter for the strip plot at the bottom
    jitter = np.random.uniform(-0.05, 0.05, size=len(nb_sizes))
    # We offset the rain below the density plot (y around -0.1)
    ax.scatter(nb_sizes, jitter - 0.1, alpha=0.1, color='teal', s=10)
    
    # 3. Boxplot
    sns.boxplot(x=nb_sizes, width=0.1, boxprops={'facecolor':'none', 'edgecolor':'black'}, zorder=10, ax=ax, orient='h')
    
    plt.title('Stochastic Extinction vs. Major Outbreak\n(Negative Binomial Superspreading Model)', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Total Outbreak Size (Log Scale)', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    
    # Remove grid lines and top/right spines
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    textstr = '\n'.join((
        rf'Extinction at Index Case: {nb_ext_index:.1f}%',
        rf'Major Cluster (>10): {nb_major:.1f}%'))
        
    plt.text(0.65, 0.85, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='lightgrey'))
            
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"appendix_stochastic_extinction_raincloud_{timestamp}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved raincloud plot to {plot_path}")

if __name__ == "__main__":
    main()
