import pandas as pd
import numpy as np
from scipy.optimize import minimize
import scipy.stats as stats

def main():
    data_path = "/Users/jasonandrews/repos/hanta/data/vial_2006_digitized_figure1.csv"
    df = pd.read_csv(data_path)
    
    # E_L is minimum incubation (time from end of exposure to onset)
    # E_R is maximum incubation (time from start of exposure to onset)
    df['E_L'] = df['symptom_onset_days']
    df['E_R'] = df['symptom_onset_days'] - df['exposure_start_days']
    
    # E_L cannot be exactly 0 for lognorm, clip at 0.1
    df['E_L'] = df['E_L'].clip(lower=0.1)
    
    def neg_log_likelihood(params):
        mu, sigma = params
        if sigma <= 0:
            return np.inf
        
        cdf_R = stats.lognorm.cdf(df['E_R'], s=sigma, scale=np.exp(mu))
        cdf_L = stats.lognorm.cdf(df['E_L'], s=sigma, scale=np.exp(mu))
        
        prob_mass = cdf_R - cdf_L
        prob_mass = np.clip(prob_mass, 1e-10, 1.0)
        
        nll = -np.sum(np.log(prob_mass))
        return nll

    initial_guess = [2.89, 0.4]
    
    result = minimize(neg_log_likelihood, initial_guess, method='L-BFGS-B', bounds=((0, 5), (0.01, 2.0)))
    
    mu_est, sigma_est = result.x
    median_incubation = np.exp(mu_est)
    
    print(f"Vial MLE results:")
    print(f"mu: {mu_est:.4f}")
    print(f"sigma: {sigma_est:.4f}")
    print(f"median: {median_incubation:.2f}")

if __name__ == "__main__":
    main()
