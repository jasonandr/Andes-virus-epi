"""Offspring distribution & Negative Binomial fit (R0, k)."""
import numpy as np
import pandas as pd
from scipy.stats import nbinom
from scipy.optimize import minimize
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

# ---- Village A: direct infector_id edges ----
A = pd.read_csv(ROOT / "data/village_a_cases.csv")
infectors_a = A["infector_id"].replace({"None": np.nan}).dropna()
counts_a = infectors_a.value_counts()
offspring_a = np.array([int(counts_a.get(cid, 0)) for cid in A["case_id"]])
print(f"Village A: n={len(offspring_a)} cases, offspring sum={offspring_a.sum()}, counts={sorted(offspring_a.tolist(), reverse=True)}")

# ---- Village B: assign each exposure to exactly one candidate infector ----
B = pd.read_csv(ROOT / "data/village_b_cases.csv")
B["exposure_date"] = pd.to_datetime(B["exposure_date"], errors="coerce")
B["date_of_onset"] = pd.to_datetime(B["date_of_onset"], errors="coerce")

# For each candidate infector (case_id), count how many distinct secondaries
# list its onset as their exposure_date. When two cases share an onset, the
# exposure is assigned to whichever case has the smaller case_id (earliest in
# the line list) — a single attribution per exposure event.
B_sorted = B.sort_values("case_id").reset_index(drop=True)
# Map each onset_date -> first case_id with that onset (the canonical infector)
canonical_infector = {}
for _, r in B_sorted.iterrows():
    o = r["date_of_onset"]
    if pd.notna(o) and o not in canonical_infector:
        canonical_infector[o] = r["case_id"]

offspring_b = {cid: 0 for cid in B["case_id"]}
unassigned = 0
for _, r in B.iterrows():
    e = r["exposure_date"]
    if pd.isna(e):
        continue
    if e in canonical_infector:
        offspring_b[canonical_infector[e]] += 1
    else:
        unassigned += 1  # exposure date with no matching onset
offspring_b_arr = np.array([offspring_b[cid] for cid in B["case_id"]])
print(f"Village B: n={len(offspring_b_arr)} cases, offspring sum={offspring_b_arr.sum()} "
      f"(unassigned exposures = {unassigned}); "
      f"counts={sorted(offspring_b_arr.tolist(), reverse=True)}")

offspring = np.concatenate([offspring_a, offspring_b_arr])
n = len(offspring)
print(f"\nCombined: n={n}, mean (empirical R0)={offspring.mean():.3f}, var={offspring.var(ddof=1):.3f}")
print(f"Histogram (0..max): {np.bincount(offspring).tolist()}")
print(f"Empirical p(0) = {(offspring==0).mean():.3f}")

def nll(params):
    log_mu, log_k = params
    mu, k = np.exp(log_mu), np.exp(log_k)
    p = k / (k + mu)
    return -np.sum(nbinom.logpmf(offspring, k, p))

x0 = [np.log(max(offspring.mean(), 0.1)), np.log(0.5)]
res = minimize(nll, x0, method="Nelder-Mead",
               options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 20000})
mu_hat, k_hat = np.exp(res.x)
print(f"\nNegative Binomial MLE:  R0 = {mu_hat:.3f}, k = {k_hat:.3f}")
print(f"Target: R0 ~0.96, k ~0.23")
p = k_hat / (k_hat + mu_hat)
print(f"P(0) under fit = {nbinom.pmf(0, k_hat, p):.3f}  (target ~0.685)")
print(f"P(1) under fit = {nbinom.pmf(1, k_hat, p):.3f}  (target ~0.126)")

out = {
    "n": int(n),
    "mean": float(offspring.mean()),
    "R0": float(mu_hat),
    "k": float(k_hat),
    "p_zero": float(nbinom.pmf(0, k_hat, p)),
    "p_one": float(nbinom.pmf(1, k_hat, p)),
    "histogram": np.bincount(offspring).tolist(),
    "village_a_offspring": offspring_a.tolist(),
    "village_b_offspring": offspring_b_arr.tolist(),
}
(ROOT / "replication/offspring_results.json").write_text(json.dumps(out, indent=2))
print("\nSaved -> replication/offspring_results.json")
