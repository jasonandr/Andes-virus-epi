import pandas as pd
import numpy as np
from scipy.optimize import minimize
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
import time
import re

def main():
    data_path = "/Users/jasonandrews/repos/hanta/data/hondius_cases.csv"
    walkthrough_path = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts/walkthrough.md"
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    
    df = pd.read_csv(data_path)
    df['date_of_onset'] = pd.to_datetime(df['date_of_onset'])
    df['exposure_start'] = pd.to_datetime(df['exposure_start'])
    df['exposure_end'] = pd.to_datetime(df['exposure_end'])
    
    # Calculate time from start of exposure to onset (max incubation)
    # and time from end of exposure to onset (min incubation)
    df['E_L'] = (df['date_of_onset'] - df['exposure_end']).dt.days
    df['E_R'] = (df['date_of_onset'] - df['exposure_start']).dt.days
    
    # Filter valid rows (where onset is after exposure start)
    df = df[df['E_R'] > 0]
    
    # E_L cannot be negative (cannot have onset before exposure ends, or if so, min incubation is 0)
    df['E_L'] = df['E_L'].clip(lower=0.1) 
    
    # Interval-censored Maximum Likelihood Estimation (Lauer et al. 2020 methodology)
    # We want to fit a Lognormal distribution to these interval censored data points.
    # The likelihood for each patient is F(E_R) - F(E_L), where F is the CDF.
    # We minimize the negative log likelihood.
    
    def neg_log_likelihood(params):
        mu, sigma = params
        if sigma <= 0:
            return np.inf
        
        # lognorm in scipy: s = sigma, scale = exp(mu)
        cdf_R = stats.lognorm.cdf(df['E_R'], s=sigma, scale=np.exp(mu))
        cdf_L = stats.lognorm.cdf(df['E_L'], s=sigma, scale=np.exp(mu))
        
        # probability mass in the interval
        prob_mass = cdf_R - cdf_L
        # Add small epsilon to avoid log(0)
        prob_mass = np.clip(prob_mass, 1e-10, 1.0)
        
        nll = -np.sum(np.log(prob_mass))
        return nll

    # Initial guess for mu and sigma (based on historical Andes data ~18 days median -> mu=2.89)
    initial_guess = [2.5, 0.5]
    
    result = minimize(neg_log_likelihood, initial_guess, method='L-BFGS-B', bounds=((0, 5), (0.01, 2.0)))
    
    mu_est, sigma_est = result.x
    median_incubation = np.exp(mu_est)
    
    # -----------------------------------------
    # Plotting the estimated distribution vs the intervals
    # -----------------------------------------
    x = np.linspace(0, 45, 500)
    pdf = stats.lognorm.pdf(x, s=sigma_est, scale=np.exp(mu_est))
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, pdf, label=f'Estimated Lognormal PDF\n(Median = {median_incubation:.1f} days)', color='purple', linewidth=2.5)
    plt.fill_between(x, pdf, alpha=0.3, color='purple')
    
    # Plot empirical intervals
    for idx, row in df.iterrows():
        plt.hlines(y=0.005 + (idx * 0.002), xmin=row['E_L'], xmax=row['E_R'], color='gray', alpha=0.5, linewidth=2)
        
    plt.title('Interval-Censored MLE of Incubation Period (Lauer et al. methodology)', fontsize=14, fontweight='bold')
    plt.xlabel('Incubation Period (Days)', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    timestamp = int(time.time())
    mle_plot_filename = f"mle_incubation_{timestamp}.png"
    mle_plot_path = os.path.join(artifacts_dir, mle_plot_filename)
    plt.savefig(mle_plot_path, dpi=300)
    plt.close()
    
    print(f"MLE completed. Estimated Median Incubation: {median_incubation:.2f} days")
    print(f"Saved MLE plot to {mle_plot_path}")
    
    # Update markdown Walkthrough
    with open(walkthrough_path, 'r') as f:
        md_content = f.read()

    if 'Advanced Estimation Models' not in md_content:
        new_md = "\n\n## Advanced Estimation Models (Lauer et al. Methodology)\n"
        new_md += "Replicating the interval-censored Maximum Likelihood Estimation approach used for COVID-19 (Annals of Internal Medicine, 2020). By leveraging the bounded exposure windows and exact symptom onset dates from our Hondius line list, we estimated the underlying Lognormal distribution of the Andes virus incubation period.\n\n"
        new_md += f"![MLE Plot]({mle_plot_path})\n"
        md_content += new_md
    else:
        md_content = re.sub(r'(!\[MLE Plot\]\()[^\)]+(\))', rf'\g<1>{mle_plot_path}\g<2>', md_content)

    with open(walkthrough_path, 'w') as f:
        f.write(md_content)

if __name__ == "__main__":
    main()
