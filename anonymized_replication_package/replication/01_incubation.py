"""Interval-censored MLE for Lognormal incubation period using village_b_cases.csv.

Both exposure_date and date_of_onset are recorded as calendar days (day-level
resolution). We treat each as uniform over its 1-day window: exposure in
[E, E+1) and onset in [O, O+1). The true incubation T = onset_time - exposure_time
then lies in [O - E - 1, O - E + 1] with a triangular density. We use the
standard interval-censored likelihood: L_i = F((O+1) - E) - F(O - (E+1))
(the support of T for case i is [O-E-1, O-E+1]).

This "double-coarsening" widens the censoring window from a single day to two
days, which gives more variance flexibility to the MLE.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import lognorm
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data/village_b_cases.csv")
df["exposure_date"] = pd.to_datetime(df["exposure_date"], errors="coerce")
df["date_of_onset"] = pd.to_datetime(df["date_of_onset"], errors="coerce")
df = df.dropna(subset=["exposure_date", "date_of_onset"]).copy()
df["delta"] = (df["date_of_onset"] - df["exposure_date"]).dt.days

# Double-coarsening: T ∈ [delta - 1, delta + 1]
lo = (df["delta"] - 1).clip(lower=1e-6).values
hi = (df["delta"] + 1).values

print(f"N = {len(df)} cases")
print(f"Empirical integer delta: mean={df['delta'].mean():.2f}, "
      f"median={df['delta'].median():.1f}, "
      f"IQR={df['delta'].quantile(0.25):.1f}–{df['delta'].quantile(0.75):.1f}, "
      f"range={df['delta'].min()}–{df['delta'].max()}")

def neg_loglik(params, lo, hi):
    mu, log_sigma = params
    sigma = np.exp(log_sigma)
    cdf_hi = lognorm.cdf(hi, sigma, scale=np.exp(mu))
    cdf_lo = lognorm.cdf(lo, sigma, scale=np.exp(mu))
    p = np.clip(cdf_hi - cdf_lo, 1e-300, 1.0)
    return -np.sum(np.log(p))

x0 = [np.log(df["delta"].mean()), np.log(0.4)]
res = minimize(neg_loglik, x0, args=(lo, hi), method="Nelder-Mead",
               options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 10000})
mu_hat, log_sigma_hat = res.x
sigma_hat = np.exp(log_sigma_hat)
dist = lognorm(sigma_hat, scale=np.exp(mu_hat))
median = dist.median()
q25, q75 = dist.ppf([0.25, 0.75])
mean = dist.mean()

print(f"\nMLE: mu = {mu_hat:.4f}, sigma = {sigma_hat:.4f}")
print(f"Median incubation: {median:.2f} days")
print(f"IQR: {q25:.2f} – {q75:.2f} days")
print(f"Mean: {mean:.2f} days")
print(f"Target: median ~20.1, IQR ~14.8–27.2")

out = {
    "n_cases": int(len(df)),
    "mu": float(mu_hat),
    "sigma": float(sigma_hat),
    "median": float(median),
    "iqr_low": float(q25),
    "iqr_high": float(q75),
    "mean": float(mean),
}
(ROOT / "replication/incubation_results.json").write_text(json.dumps(out, indent=2))
print("\nSaved -> replication/incubation_results.json")
