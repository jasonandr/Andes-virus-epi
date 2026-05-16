"""Generate replication figures matching figure_1 and figure_2."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm, nbinom, gaussian_kde, poisson
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "replication"

inc = json.loads((OUT / "incubation_results.json").read_text())
ser = json.loads((OUT / "serial_results.json").read_text())
off = json.loads((OUT / "offspring_results.json").read_text())

inc_dist = lognorm(inc["sigma"], scale=np.exp(inc["mu"]))
# Reference "environmental" incubation: median ~18.5
env_mu = np.log(18.5)
env_sigma = inc["sigma"]  # assume similar spread
env_dist = lognorm(env_sigma, scale=np.exp(env_mu))

tost = np.load(OUT / "tost_samples.npy")
outbreak_sizes = np.load(OUT / "outbreak_sizes.npy")

# ------------------------------------------------------------------
# Figure 1: A) Incubation density, B) Infectiousness profile, C) NB fit
# ------------------------------------------------------------------
fig, axes = plt.subplots(3, 1, figsize=(8, 14))

# Panel A: incubation
ax = axes[0]
x = np.linspace(0.1, 60, 400)
ax.fill_between(x, env_dist.pdf(x), color="#7AC36A", alpha=0.55, label="Environmental Exposure")
ax.fill_between(x, inc_dist.pdf(x), color="#5A9BD5", alpha=0.55, label="Human-to-Human Contact")
ax.axvline(env_dist.median(), color="green", linestyle="--", linewidth=1.5)
ax.axvline(inc_dist.median(), color="blue", linestyle="--", linewidth=1.5)
ax.set_xlabel("Incubation Period (Days)")
ax.set_ylabel("Probability Density")
ax.set_title("A", loc="left", fontweight="bold")
ax.legend()
ax.set_xlim(0, 60)

# Panel B: infectiousness profile (TOST density)
ax = axes[1]
kde = gaussian_kde(tost, bw_method=0.18)
xt = np.linspace(tost.min(), tost.max(), 400)
ax.fill_between(xt, kde(xt), color="#C0504D", alpha=0.55)
ax.plot(xt, kde(xt), color="#C0504D", linewidth=1.8, label="Infectiousness Profile")
ax.axvline(0, color="black", linestyle="--", linewidth=1.5, label="Symptom Onset")
ax.set_xlabel("Days Relative to Symptom Onset")
ax.set_ylabel("Relative Infectiousness")
ax.set_title("B", loc="left", fontweight="bold")
ax.legend()
ax.set_xlim(-20, 35)

# Panel C: offspring distribution histogram + NB fit + Poisson
ax = axes[2]
village_a = np.array(off["village_a_offspring"])
village_b = np.array(off["village_b_offspring"])
maxv = max(village_a.max(), village_b.max())
bins = np.arange(-0.5, maxv + 1.5, 1)
ax.hist(village_b, bins=bins, alpha=0.55, color="#5B9BB0", label="2018 Epuyén", edgecolor="white")
ax.hist(village_a, bins=bins, alpha=0.55, color="#8B4543", label="1996 El Bolsón", edgecolor="white")
xs = np.arange(0, maxv + 1)
R0, k = off["R0"], off["k"]
p = k / (k + R0)
nb_pmf = nbinom.pmf(xs, k, p)
poi_pmf = poisson.pmf(xs, R0)
N = len(village_a) + len(village_b)
ax.plot(xs, nb_pmf * N, "k--", linewidth=2, label=f"Negative Binomial Fit\n(k = {k:.2f}, Superspreading)")
ax.plot(xs, poi_pmf * N, ":", color="#C0504D", linewidth=2, label="Poisson Fit\n(k → ∞, Homogeneous)")
ax.set_xlabel("Number of Secondary Cases per Infectious Individual")
ax.set_ylabel("Frequency")
ax.set_title("C", loc="left", fontweight="bold")
ax.legend(fontsize=8)
ax.set_xlim(-0.5, maxv + 0.5)

plt.tight_layout()
plt.savefig(OUT / "figure_1_combined_analysis.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved figure_1_combined_analysis.png")

# ------------------------------------------------------------------
# Figure 2: Raincloud of outbreak sizes (log scale)
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
log_sizes = np.log10(outbreak_sizes)
xs = np.linspace(log_sizes.min() - 0.1, log_sizes.max() + 0.1, 600)
kde = gaussian_kde(log_sizes, bw_method=0.08)
density = kde(xs)
ax.fill_between(xs, density, color="#3F8B8B", alpha=0.7)
ax.plot(xs, density, color="#2D6F6F", linewidth=1.5)

# strip rug
y_rug = -0.05
jitter = (np.random.default_rng(1).uniform(-0.04, 0.04, size=len(outbreak_sizes)))
ax.scatter(log_sizes + np.random.default_rng(2).uniform(-0.005, 0.005, size=len(outbreak_sizes)),
           np.full_like(log_sizes, y_rug, dtype=float) + jitter,
           s=2, color="#3F8B8B", alpha=0.05)

# boxplot
bp = ax.boxplot(log_sizes, vert=False, positions=[-0.18], widths=0.06, showfliers=False,
                patch_artist=False)
for line in bp["medians"]:
    line.set_color("black")

ax.set_xlabel("Total Outbreak Size")
ax.set_ylabel("Relative Density")
xticks = [0, 1, 2, 3]
ax.set_xticks(xticks)
ax.set_xticklabels([f"{10**t:g}" for t in xticks])
ax.set_yticks([])
ax.set_ylim(-0.25, max(density) * 1.1)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
plt.tight_layout()
plt.savefig(OUT / "figure_2_stochastic_extinction.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("Saved figure_2_stochastic_extinction.png")
