import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
import time

def simulate_outbreak(R0, k=None, max_generations=20, max_cases=500):
    """
    Simulate a branching process outbreak.
    If k is None, use Poisson. Otherwise use Negative Binomial.
    Returns total outbreak size.
    """
    current_cases = 1
    total_cases = 1
    
    for gen in range(max_generations):
        if current_cases == 0:
            break
            
        if k is None:
            # Poisson
            next_gen_cases = np.sum(np.random.poisson(R0, current_cases))
        else:
            # Negative Binomial
            p = k / (k + R0)
            next_gen_cases = np.sum(np.random.negative_binomial(k, p, current_cases))
            
        current_cases = next_gen_cases
        total_cases += current_cases
        
        if total_cases >= max_cases:
            return max_cases # Cap to avoid infinite loops if R0 > 1
            
    return total_cases

def main():
    R0 = 0.96
    k = 0.23
    num_sims = 10000
    
    nb_sizes = []
    poisson_sizes = []
    
    np.random.seed(42)
    
    for _ in range(num_sims):
        nb_sizes.append(simulate_outbreak(R0, k=k))
        poisson_sizes.append(simulate_outbreak(R0, k=None))
        
    nb_sizes = np.array(nb_sizes)
    poisson_sizes = np.array(poisson_sizes)
    
    # Calculate probabilities
    # 1. Extinction at index case (total size = 1)
    nb_ext_index = np.mean(nb_sizes == 1) * 100
    p_ext_index = np.mean(poisson_sizes == 1) * 100
    
    # 2. Major outbreak (>10 cases)
    nb_major = np.mean(nb_sizes > 10) * 100
    p_major = np.mean(poisson_sizes > 10) * 100
    
    # Plotting
    plt.figure(figsize=(10, 6))
    
    bins = np.logspace(0, 3, 30)
    plt.hist(poisson_sizes, bins=bins, alpha=0.5, label='Homogenous (Poisson)', color='red', density=True)
    plt.hist(nb_sizes, bins=bins, alpha=0.5, label=f'Superspreading (NegBinom, k={k})', color='blue', density=True)
    
    plt.xscale('log')
    plt.yscale('log')
    
    plt.title('Stochastic Extinction vs. Major Outbreak\n(10,000 Branching Process Simulations)', fontsize=14, fontweight='bold')
    plt.xlabel('Total Outbreak Size (Log Scale)', fontsize=12)
    plt.ylabel('Probability Density (Log Scale)', fontsize=12)
    
    textstr = '\n'.join((
        r'Extinction at Index Case (Size = 1):',
        rf'  Homogenous: {p_ext_index:.1f}%',
        rf'  Superspreading: {nb_ext_index:.1f}%',
        r'',
        r'Probability of Major Cluster (>10):',
        rf'  Homogenous: {p_major:.1f}%',
        rf'  Superspreading: {nb_major:.1f}%'))
        
    plt.text(0.55, 0.95, textstr, transform=plt.gca().transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
    plt.legend(loc='center right')
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"appendix_stochastic_extinction_{timestamp}.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved stochastic extinction simulation to {plot_path}")

if __name__ == "__main__":
    main()
