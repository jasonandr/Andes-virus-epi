"""Search exposure-window widths to identify which one the reference analysis used."""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import lognorm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data/village_b_cases.csv")
df["exposure_date"] = pd.to_datetime(df["exposure_date"], errors="coerce")
df["date_of_onset"] = pd.to_datetime(df["date_of_onset"], errors="coerce")
df = df.dropna(subset=["exposure_date", "date_of_onset"]).copy()
df["delta"] = (df["date_of_onset"] - df["exposure_date"]).dt.days

def fit(lo, hi):
    def nll(p):
        sigma = np.exp(p[1])
        L = lognorm.cdf(hi, sigma, scale=np.exp(p[0])) - lognorm.cdf(lo, sigma, scale=np.exp(p[0]))
        return -np.sum(np.log(np.clip(L, 1e-300, 1)))
    r = minimize(nll, [np.log(df['delta'].mean()), np.log(0.4)], method="Nelder-Mead",
                 options={"xatol":1e-9,"fatol":1e-9,"maxiter":10000})
    mu, lsig = r.x
    d = lognorm(np.exp(lsig), scale=np.exp(mu))
    return d.median(), *d.ppf([0.25,0.75])

print(f"{'window':>20}  {'median':>7}  {'q25':>7}  {'q75':>7}")
# Symmetric around exposure_date (E-W to E)
for W in [0.5, 1, 2, 3, 5, 7, 10, 14]:
    lo = (df['delta'] - 0.5).clip(lower=1e-6).values
    hi = (df['delta'] + W + 0.5).values  # exposure could be up to W days before listed E
    m, q1, q3 = fit(lo, hi)
    print(f"  E in [E-{W}, E]   m={m:.2f}  IQR=[{q1:.2f},{q3:.2f}]")

print()
for W in [0.5, 1, 2, 3, 5, 7, 10, 14]:
    # symmetric: exposure in [E-W, E+W]
    lo = (df['delta'] - W - 0.5).clip(lower=1e-6).values
    hi = (df['delta'] + W + 0.5).values
    m, q1, q3 = fit(lo, hi)
    print(f"  E ± {W}d sym       m={m:.2f}  IQR=[{q1:.2f},{q3:.2f}]")

print()
# Onset uncertain too: T in [O - E - W, O+1 - E]
for W in [0.5, 1, 2, 3, 5, 7, 10, 14]:
    lo = (df['delta'] - W).clip(lower=1e-6).values
    hi = (df['delta'] + 1).values
    m, q1, q3 = fit(lo, hi)
    print(f"  exp window {W}d back  m={m:.2f}  IQR=[{q1:.2f},{q3:.2f}]")
