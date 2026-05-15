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
    num_sims = 50000
    
    np.random.seed(42)
    nb_sizes = np.array([simulate_outbreak(R0, k, max_cases=5000) for _ in range(num_sims)])
    
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    
    log_sizes = np.log10(nb_sizes)
    kde = stats.gaussian_kde(log_sizes)
    x_eval = np.linspace(np.log10(0.8), np.log10(5000), 1000)
    y_eval = kde(x_eval)
    
    max_y = np.max(y_eval)
    
    ax.fill_between(10**x_eval, 0, y_eval, color='teal', alpha=0.5)
    ax.plot(10**x_eval, y_eval, color='teal', linewidth=2)
    
    jitter = np.random.uniform(-max_y*0.2, -max_y*0.05, size=len(nb_sizes))
    ax.scatter(nb_sizes, jitter, alpha=0.01, color='teal', s=10, zorder=0)
    
    ax.boxplot(nb_sizes, vert=False, positions=[-max_y*0.3], widths=[max_y*0.1], 
               manage_ticks=False, patch_artist=True, showfliers=False,
               boxprops=dict(facecolor='none', color='black', linewidth=1.5),
               whiskerprops=dict(color='black', linewidth=1.5),
               capprops=dict(color='black', linewidth=1.5),
               medianprops=dict(color='black', linewidth=2.5))
               
    ax.set_xscale('log')
    ax.set_xticks([1, 10, 100, 1000])
    ax.set_xticklabels(['1', '10', '100', '1000'])
    ax.set_ylim(-max_y*0.4, max_y * 1.1)
    ax.set_yticks([]) 
    
    plt.title('D. Stochastic Extinction vs. Major Outbreak (Superspreading Model)', fontsize=14, fontweight='bold')
    plt.xlabel('Total Outbreak Size', fontsize=12)
    plt.ylabel('Relative Density', fontsize=12)
    
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
            
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"appendix_stochastic_extinction_raincloud_{timestamp}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved raincloud plot to {plot_path}")

if __name__ == "__main__":
    main()
