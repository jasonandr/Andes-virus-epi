import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
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
    ax = plt.gca()
    
    # 1. Calculate KDE for the "Cloud"
    # We do KDE in log space since the data spans orders of magnitude
    log_sizes = np.log10(nb_sizes)
    kde = stats.gaussian_kde(log_sizes)
    x_eval = np.linspace(np.log10(0.8), np.log10(1000), 1000)
    y_eval = kde(x_eval)
    
    max_y = np.max(y_eval)
    
    # Plot the Cloud
    ax.fill_between(10**x_eval, 0, y_eval, color='teal', alpha=0.5)
    ax.plot(10**x_eval, y_eval, color='teal', linewidth=2)
    
    # 2. Strip Plot (The "Rain")
    # Put rain below the cloud
    jitter = np.random.uniform(-max_y*0.2, -max_y*0.05, size=len(nb_sizes))
    ax.scatter(nb_sizes, jitter, alpha=0.05, color='teal', s=15, zorder=0)
    
    # 3. Boxplot
    # Positioned below the rain
    ax.boxplot(nb_sizes, vert=False, positions=[-max_y*0.3], widths=[max_y*0.1], 
               manage_ticks=False, patch_artist=True, showfliers=False,
               boxprops=dict(facecolor='none', color='black', linewidth=1.5),
               whiskerprops=dict(color='black', linewidth=1.5),
               capprops=dict(color='black', linewidth=1.5),
               medianprops=dict(color='black', linewidth=2.5))
               
    ax.set_xscale('log')
    ax.set_ylim(-max_y*0.4, max_y * 1.1)
    ax.set_yticks([]) # Hide y-axis ticks since density is relative
    
    plt.title('Stochastic Extinction vs. Major Outbreak\n(Negative Binomial Superspreading Model)', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Total Outbreak Size (Log Scale)', fontsize=12)
    plt.ylabel('Relative Density', fontsize=12)
    
    # Remove grid lines and top/right/left spines
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
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
