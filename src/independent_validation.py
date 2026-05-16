import pandas as pd
import numpy as np
import scipy.stats as stats
import os

def main():
    print("="*60)
    print("INDEPENDENT PARALLEL VALIDATION REPORT")
    print("="*60)

    # 1. Validate Incubation Period (Epuyen 2018)
    # Using scipy.stats.lognorm.fit instead of custom MLE interval-censoring
    try:
        epuyen_df = pd.read_csv('../data/epuyen_2018_actual_cases_parsed.csv')
        epuyen_df = epuyen_df.dropna(subset=['exposure_date', 'date_of_onset'])
        
        incubation_days = []
        for idx, row in epuyen_df.iterrows():
            exp = pd.to_datetime(row['exposure_date'])
            onset = pd.to_datetime(row['date_of_onset'])
            incubation_days.append((onset - exp).days)
            
        data = np.array(incubation_days)
        
        # Fit Lognormal
        # lognorm.fit returns shape, loc, scale. median = scale.
        shape, loc, scale = stats.lognorm.fit(data, floc=0)
        
        print("\n1. INCUBATION PERIOD VALIDATION")
        print("Method: Scipy Lognormal fit on exact exposure dates (non-interval-censored)")
        print(f"Sample Size: {len(data)}")
        print(f"Mean Incubation: {np.mean(data):.1f} days")
        print(f"Median Incubation (Analytical Scale): {scale:.1f} days")
        print(f"-> Original Manuscript claimed: 20.1 days")
        diff = abs(scale - 20.1)
        if diff < 1.0:
            print("-> STATUS: VALIDATED (Diff < 1 day)")
        else:
            print(f"-> STATUS: DISCREPANCY ({diff:.1f} days)")
            
    except Exception as e:
        print(f"Incubation validation failed: {e}")

    # 2. Validate Offspring Distribution (R0 and k)
    try:
        # Load El Bolson
        eb_df = pd.read_csv('../data/el_bolson_1996_cases.csv')
        eb_infectors = eb_df['infector_id'].dropna().astype(str).tolist()
        eb_cases = eb_df['case_id'].dropna().astype(str).tolist()
        
        secondary_counts = []
        for c in eb_cases:
            secondary_counts.append(eb_infectors.count(c))
            
        # Try to add Epuyen data
        if os.path.exists('../data/epuyen_2018_cases.csv'):
            ep_df = pd.read_csv('../data/epuyen_2018_cases.csv')
            if 'infector_id' in ep_df.columns and 'case_id' in ep_df.columns:
                ep_infectors = ep_df['infector_id'].dropna().astype(str).tolist()
                ep_cases = ep_df['case_id'].dropna().astype(str).tolist()
                for c in ep_cases:
                    secondary_counts.append(ep_infectors.count(c))
                    
        # Now we have the offspring distribution array
        counts = np.array(secondary_counts)
        mean_R0 = np.mean(counts)
        variance = np.var(counts)
        
        # Method of Moments is biased for superspreading; use MLE
        from scipy.optimize import minimize
        def neg_log_likelihood(params):
            R0, k = params
            if R0 <= 0 or k <= 0: return np.inf
            p = k / (k + R0)
            return -np.sum(stats.nbinom.logpmf(counts, n=k, p=p))
            
        initial_guess = [mean_R0, 1.0]
        result = minimize(neg_log_likelihood, initial_guess, bounds=((0.01, 10), (0.01, 10)))
        R0_mle, k_mle = result.x
            
        print("\n2. OFFSPRING DISTRIBUTION VALIDATION (R0 and k)")
        print("Method: Independent MLE Negative Binomial Fit")
        print(f"Total Cases Assessed: {len(counts)}")
        print(f"Calculated Mean (R0): {R0_mle:.2f}")
        print(f"Calculated Dispersion (k): {k_mle:.3f}")
        print(f"-> Original Manuscript claimed: R0 = 0.96, k = 0.23")
        
        diff_r0 = abs(R0_mle - 0.96)
        diff_k = abs(k_mle - 0.23)
        
        if diff_r0 < 0.1 and diff_k < 0.1:
            print("-> STATUS: VALIDATED (Diffs < 0.1)")
        else:
            print(f"-> STATUS: DISCREPANCY (R0 diff: {diff_r0:.2f}, k diff: {diff_k:.2f})")

        # 3. Validate Immediate Extinction Probability
        # P(X = 0) for Negative Binomial = (1 + R0/k)^(-k)
        analytical_extinction = (1 + R0_mle / k_mle)**(-k_mle) * 100
        
        print("\n3. STOCHASTIC EXTINCTION VALIDATION")
        print("Method: Analytical PMF vs Original 50,000-iteration Branching Process Simulation")
        print(f"Analytical P(X=0): {analytical_extinction:.1f}%")
        print(f"-> Original Manuscript claimed: 78.5%")
        
        diff_ext = abs(analytical_extinction - 78.5)
        if diff_ext < 2.0:
            print("-> STATUS: VALIDATED (Diff < 2.0%)")
        else:
            print(f"-> STATUS: DISCREPANCY ({diff_ext:.1f}%)")

    except Exception as e:
        print(f"Transmission validation failed: {e}")

    print("="*60)

if __name__ == "__main__":
    # run from src
    if os.path.basename(os.getcwd()) != 'src':
        os.chdir('src')
    main()
