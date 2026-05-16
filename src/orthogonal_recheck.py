import numpy as np
import pandas as pd
from scipy.optimize import minimize
import scipy.stats as stats
import pdfplumber

def get_epuyen_secondary_counts():
    counts = []
    with pdfplumber.open('literature/nejmoa2009040_appendix_1.pdf') as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split('\n'):
                    if line.startswith('Patient '):
                        parts = line.split()
                        try:
                            int(parts[1])
                            if len(parts) > 5 and ('2018' in line or '2019' in line):
                                counts.append(int(parts[-1]))
                        except:
                            pass
    return counts

def get_el_bolson_secondary_counts():
    df = pd.read_csv('data/el_bolson_1996_cases.csv')
    infectors = df['infector_id'].dropna().astype(str).tolist()
    # The list of ALL unique individuals (index + cases)
    # The index case 'I' is in the dataset.
    all_cases = df['case_id'].dropna().astype(str).tolist()
    
    counts = []
    for c in all_cases:
        counts.append(infectors.count(c))
    return counts

def main():
    print("="*50)
    print("ORTHOGONAL RECHECK REPORT")
    print("="*50)

    ep_counts = get_epuyen_secondary_counts()
    eb_counts = get_el_bolson_secondary_counts()
    
    combined = np.array(ep_counts + eb_counts)
    
    print(f"Total Epuyén Cases: {len(ep_counts)}")
    print(f"Total El Bolsón Cases: {len(eb_counts)}")
    print(f"Combined Sample Size: {len(combined)}")
    print(f"Total Secondary Infections: {sum(combined)}")
    
    R0 = np.mean(combined)
    print(f"\nEmpirical R0 = {R0:.4f}")
    
    def nll(params):
        R_est, k_est = params
        if R_est <= 0 or k_est <= 0: return np.inf
        p = k_est / (k_est + R_est)
        return -np.sum(stats.nbinom.logpmf(combined, n=k_est, p=p))
        
    res = minimize(nll, [R0, 1.0], bounds=((0.01, 10), (0.01, 10)))
    k_mle = res.x[1]
    
    print(f"MLE Dispersion k = {k_mle:.4f}")
    
    # Probability of zero secondary cases
    p_zero = (1 + R0/k_mle)**(-k_mle) * 100
    print(f"Probability of Immediate Extinction P(X=0) = {p_zero:.2f}%")
    
    print("="*50)

if __name__ == '__main__':
    main()
