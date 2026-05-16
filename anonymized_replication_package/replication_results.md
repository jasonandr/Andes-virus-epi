# Expected Replication Results

Once you have completed the tasks outlined in `analysis_instructions.md`, verify your findings against these validated benchmarks. If your code operates correctly, your results should tightly match the following parameters and visual profiles.

## 1. Incubation Period (Interval-Censored MLE)
- **Median Incubation Period:** ~20.1 days
- **Interquartile Range (IQR):** ~14.8 to 27.2 days
*Finding:* The incubation period is exceptionally long. If you model an environmental exposure benchmark (median 18.5 days), you will find the density functions are nearly identical, indicating the extended timeline is intrinsic to the pathogenesis of Pathogen X regardless of exposure route.

## 2. Infectiousness Profile and Serial Interval
- **Mean Serial Interval:** ~26.5 days
- **Presymptomatic Transmission:** ~24%
*Finding:* Approximately a quarter of transmission events occur in the presymptomatic or late prodromal phase, highlighting the extreme risk in dense environments like a cruise ship where individuals mix socially before severe illness begins.

## 3. Transmission Heterogeneity
- **Basic Reproduction Number ($R_0$):** ~0.96
- **Dispersion Parameter ($k$):** ~0.23
*Finding:* The dispersion parameter is extremely low ($k < 1.0$), which is the mathematical hallmark of superspreading. The vast majority of infected individuals (>80%) transmit the virus to zero or exactly one other person (specifically, ~68.5% generate zero cases and ~12.6% generate one case), while a small minority are responsible for multi-generational transmission chains.

## 4. Stochastic Extinction Simulation
- **Probability of Stochastic Extinction:** ~68.5%
*Finding:* Because of the high transmission heterogeneity, if a single case is introduced into an isolated environment, there is a very high probability (68.5%) that the transmission chain will naturally terminate at the index case without generating any secondary infections. However, the outbreaks that survive the first generation exhibit long-tail epidemic growth (as seen in the accompanying unlabelled raincloud plot).

## Reference Figures
You can find the target output figures located in the `figures/` directory. Your generated plots should mirror these statistical distributions:
- `figure_1_combined_analysis.png`: Contains the Lognormal MLE density curves, the deconvoluted infectiousness profile, and the Negative Binomial fit.
- `figure_2_stochastic_extinction.png`: A raincloud plot of outbreak sizes showing the long-tail distribution from the branching simulation.
- `figure_3_cruise_timeline.png`: The empirical Gantt chart of the ongoing outbreak you are assessing.
- `figure_4_demographics.png`: A demographic profile of infectiousness, demonstrating no linear correlation between age and the number of secondary cases.
