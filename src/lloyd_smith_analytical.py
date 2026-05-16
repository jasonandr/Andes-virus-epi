import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
import time

def main():
    k = 0.23
    
    # Proportion of cases (most infectious first)
    # We want x from 0 to 1. 
    x = np.linspace(0.0001, 1, 1000)
    
    # 1. Find the individual reproduction number threshold v_x
    # for the top x proportion of cases.
    # v_x is the (1-x) quantile of the Gamma(k) distribution.
    # Note: scale doesn't matter for the proportion, we can set scale=1.
    v_x = stats.gamma.ppf(1 - x, a=k)
    
    # 2. The proportion of expected transmission caused by individuals with v > v_x
    # is the upper tail of the Gamma(k+1) distribution.
    y = 1 - stats.gamma.cdf(v_x, a=k+1)
    
    plt.figure(figsize=(10, 8))
    
    # Plot Andes Virus theoretical curve
    plt.plot(x, y, color='darkred', linewidth=3, label=f'Andes Virus ($k={k}$)')
    
    # Plot Homogeneous transmission (Dirac delta for v)
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--', linewidth=2, label='Homogeneous (Line of Equality)')
    
    # 20/80 Rule Line
    # Calculate what the top 20% cause theoretically
    v_20 = stats.gamma.ppf(0.8, a=k)
    y_20 = 1 - stats.gamma.cdf(v_20, a=k+1)
    
    plt.axvline(x=0.2, color='black', linestyle=':', alpha=0.5)
    plt.axhline(y=y_20, color='black', linestyle=':', alpha=0.5)
    plt.scatter([0.2], [y_20], color='black', zorder=5, s=50)
    
    plt.text(0.22, y_20 - 0.03, f'Top 20% of cases cause\n{y_20*100:.1f}% of transmission', fontsize=16, fontweight='bold')
    
    # Aesthetics
    plt.title('D', loc='left', fontsize=22, fontweight='bold')
    plt.xlabel('Proportion of cases', fontsize=17)
    plt.ylabel('Expected proportion of transmission', fontsize=17)
    
    plt.xlim(0, 1)
    plt.ylim(0, 1.05)
    plt.legend(loc='lower right', fontsize=16)
    plt.grid(True, alpha=0.3)
    
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"lloyd_smith_analytical_{timestamp}.png")
    plt.savefig(plot_path, dpi=300)
    
    # Also save to figures folder
    os.makedirs('figures', exist_ok=True)
    plt.savefig('figures/lloyd_smith_curve.png', dpi=300)
    plt.close()
    
    print(f"Saved Analytical Lloyd-Smith plot to {plot_path}")
    print(f"Top 20% transmission: {y_20*100:.1f}%")

if __name__ == "__main__":
    main()
