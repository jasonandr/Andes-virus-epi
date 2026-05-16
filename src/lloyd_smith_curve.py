import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
import time
import re

def main():
    R0 = 0.96
    k = 0.23
    
    # Simulate a very large cohort to construct the Lorenz curve
    N = 1000000
    p = k / (k + R0)
    
    # Sample offspring distribution
    samples = stats.nbinom.rvs(n=k, p=p, size=N)
    
    # Sort descending (most infectious first)
    samples_sorted = np.sort(samples)[::-1]
    
    # Cumulative proportion of transmission
    cum_transmission = np.cumsum(samples_sorted)
    prop_transmission = cum_transmission / cum_transmission[-1]
    
    # Cumulative proportion of cases
    prop_cases = np.arange(1, N + 1) / N
    
    # Plotting
    plt.figure(figsize=(8, 8))
    
    # Plot Andes Virus curve
    plt.plot(prop_cases, prop_transmission, color='darkred', linewidth=3, label=f'Andes Virus ($R_0$={R0}, $k$={k})')
    
    # Plot homogenous (Poisson) curve for reference (k -> infinity)
    samples_poisson = stats.poisson.rvs(mu=R0, size=N)
    samples_poisson_sorted = np.sort(samples_poisson)[::-1]
    cum_poisson = np.cumsum(samples_poisson_sorted)
    prop_poisson = cum_poisson / cum_poisson[-1]
    
    plt.plot(prop_cases, prop_poisson, color='gray', linestyle='--', linewidth=2, label='Homogeneous Transmission (Poisson)')
    
    # Calculate what the top 20% cause
    idx_20 = int(0.2 * N)
    prop_trans_20 = prop_transmission[idx_20]
    
    plt.axvline(x=0.2, color='black', linestyle=':', alpha=0.5)
    plt.axhline(y=prop_trans_20, color='black', linestyle=':', alpha=0.5)
    plt.scatter([0.2], [prop_trans_20], color='black', zorder=5, s=50)
    
    plt.text(0.22, prop_trans_20 - 0.03, f'Top 20% of cases cause\n{prop_trans_20*100:.1f}% of transmission', fontsize=16, fontweight='bold')
    
    # Aesthetics
    plt.title('Lloyd-Smith Extent of Superspreading (Figure 1b)', fontsize=15, fontweight='bold')
    plt.xlabel('Proportion of Cases (Sorted by most infectious first)', fontsize=17)
    plt.ylabel('Expected Proportion of Total Transmission', fontsize=17)
    
    plt.xlim(0, 1)
    plt.ylim(0, 1.05)
    plt.legend(loc='lower right', fontsize=16)
    plt.grid(True, alpha=0.3)
    
    # Clean up spines
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_filename = f"lloyd_smith_curve_{timestamp}.png"
    plot_path = os.path.join(artifacts_dir, plot_filename)
    plt.savefig(plot_path, dpi=300)
    plt.close()
    
    print(f"Saved Lloyd-Smith plot to {plot_path}")
    print(f"Top 20% transmission: {prop_trans_20*100:.1f}%")
    
    # Append to walkthrough
    walkthrough_path = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts/walkthrough.md"
    if os.path.exists(walkthrough_path):
        with open(walkthrough_path, 'r') as f:
            content = f.read()
            
        if "Lloyd-Smith Curve" in content:
            content = re.sub(r'(!\[Lloyd-Smith Curve\]\()[^\)]+(\))', rf'\g<1>{plot_path}\g<2>', content)
        else:
            content += "\n\n## Lloyd-Smith Extent of Superspreading\n"
            content += "Mirroring Figure 1b of Lloyd-Smith et al. (2005), this curve visually demonstrates transmission heterogeneity. It plots the expected proportion of transmission caused by the top $x$ proportion of most infectious cases.\n\n"
            content += f"![Lloyd-Smith Curve]({plot_path})\n"
            
        with open(walkthrough_path, 'w') as f:
            f.write(content)

if __name__ == "__main__":
    main()
