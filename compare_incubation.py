import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import os
import time

def main():
    # Environmental Incubation (Vial et al., 2006)
    # Median 18.5 days. Lognormal parameters: mu = ln(18.5) = 2.917
    # 95% range 7-39 days implies sigma ~ 0.43
    env_mu = np.log(18.5)
    env_sigma = 0.43
    
    # H2H Incubation (Our MLE from 2018 Epuyén Data)
    # Median 20.17 days. mu = ln(20.17) = 3.004
    # Our estimated sigma was approx 0.45
    h2h_mu = np.log(20.17)
    h2h_sigma = 0.45
    
    x = np.linspace(0.1, 60, 1000)
    
    env_pdf = stats.lognorm.pdf(x, s=env_sigma, scale=np.exp(env_mu))
    h2h_pdf = stats.lognorm.pdf(x, s=h2h_sigma, scale=np.exp(h2h_mu))
    
    plt.figure(figsize=(10, 6))
    
    plt.fill_between(x, env_pdf, color='forestgreen', alpha=0.4, label='Environmental Exposure')
    plt.plot(x, env_pdf, color='darkgreen', linewidth=2)
    
    plt.fill_between(x, h2h_pdf, color='steelblue', alpha=0.4, label='Human-to-Human Contact')
    plt.plot(x, h2h_pdf, color='midnightblue', linewidth=2)
    
    plt.axvline(x=18.5, color='darkgreen', linestyle='--', alpha=0.7)
    plt.axvline(x=20.17, color='midnightblue', linestyle='--', alpha=0.7)
    
    plt.title('A. Comparative Incubation Periods (Environmental vs. Human-to-Human)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Incubation Period (Days)', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    
    # Clean up plot
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.grid(axis='y', alpha=0.3)
    
    plt.legend(loc='upper right', fontsize=11, framealpha=0.9)
    plt.xlim(0, 60)
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"comparative_incubation_{timestamp}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved comparative incubation plot to {plot_path}")

if __name__ == "__main__":
    main()
