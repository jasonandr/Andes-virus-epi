"""Stochastic branching process simulation.

Each generation, every infectious individual generates X ~ NegBin(R0, k)
secondary cases. Start from 1 index case. Run for many iterations and capture
total outbreak size (sum across all generations until extinction or cap).
"""
import numpy as np
from scipy.stats import nbinom
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
res = json.loads((ROOT / "replication/offspring_results.json").read_text())
R0, k = res["R0"], res["k"]
print(f"Using R0 = {R0:.3f}, k = {k:.3f}")

rng = np.random.default_rng(20260515)
N_ITER = 50_000
MAX_SIZE = 5_000  # cap to keep simulations bounded
MAX_GEN = 200

p_param = k / (k + R0)

def simulate_once(rng):
    infectious = 1
    total = 1
    gen = 0
    first_gen_offspring = -1
    while infectious > 0 and total < MAX_SIZE and gen < MAX_GEN:
        new_cases = nbinom.rvs(k, p_param, size=infectious, random_state=rng).sum()
        if gen == 0:
            first_gen_offspring = int(new_cases)
        infectious = new_cases
        total += new_cases
        gen += 1
    return total, first_gen_offspring, gen

sizes = np.empty(N_ITER, dtype=np.int64)
first_gen = np.empty(N_ITER, dtype=np.int32)
for i in range(N_ITER):
    s, fg, _ = simulate_once(rng)
    sizes[i] = s
    first_gen[i] = fg

p_extinct = float((first_gen == 0).mean())
print(f"\nN = {N_ITER:,} simulations")
print(f"P(immediate extinction, i.e. 0 offspring in gen 1) = {p_extinct:.4f}  (target ~0.685)")
print(f"P(outbreak size = 1)                                = {(sizes == 1).mean():.4f}")
print(f"Mean outbreak size                                  = {sizes.mean():.2f}")
print(f"Median outbreak size                                = {np.median(sizes):.1f}")
print(f"Max observed outbreak size                          = {sizes.max()}")
print(f"P(outbreak ≥ 100)                                   = {(sizes >= 100).mean():.4f}")
print(f"P(hit cap of {MAX_SIZE})                             = {(sizes >= MAX_SIZE).mean():.4f}")

out = {
    "n_iter": N_ITER,
    "R0": R0,
    "k": k,
    "prob_extinction_immediate": p_extinct,
    "mean_size": float(sizes.mean()),
    "median_size": float(np.median(sizes)),
    "max_size": int(sizes.max()),
    "p_size_geq_100": float((sizes >= 100).mean()),
    "p_hit_cap": float((sizes >= MAX_SIZE).mean()),
}
(ROOT / "replication/branching_results.json").write_text(json.dumps(out, indent=2))
np.save(ROOT / "replication/outbreak_sizes.npy", sizes)
print("\nSaved -> replication/branching_results.json + outbreak_sizes.npy")
