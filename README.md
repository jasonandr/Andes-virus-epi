# Andes Virus Transmission Dynamics

This repository contains the epidemiological data, statistical models, and branching process simulations underpinning the rapid communication regarding the Andes orthohantavirus (ANDV) cluster aboard the MV Hondius.

## Overview
Unlike most hantaviruses, which are exclusively transmitted via aerosolized rodent excreta, ANDV is capable of human-to-human transmission. To quantify the specific risks this poses to high-density environments like cruise ships, we analyzed the two most extensively documented historical outbreaks: the 1996 cluster in El Bolsón and the 2018–2019 outbreak in Epuyén, Argentina.

## Key Findings
1. **Prolonged Incubation:** Interval-censored Maximum Likelihood Estimation (MLE) of bounded social exposures reveals a median human-to-human incubation period of 20.1 days, remarkably similar to environmental exposures (18.5 days).
2. **Presymptomatic Shedding:** Deconvolution of empirical serial intervals demonstrates that ~24% of transmission occurs prior to the onset of severe febrile illness.
3. **Extreme Transmission Heterogeneity:** Negative binomial regression of the offspring distribution yields an $R_0 = 0.96$ and a dispersion parameter of $k = 0.23$. Over 80% of infected individuals generate 0 or 1 secondary cases, while a minority of "super-spreaders" are responsible for massive multi-generational transmission chains.
4. **Stochastic Extinction:** Branching process simulations show that, despite superspreading risk, 68.5% of single-case introductions result in immediate stochastic extinction.

## Repository Structure
* `/data/`: Raw and parsed line lists from historical outbreaks (El Bolsón 1996, Epuyén 2018) and the MV Hondius cluster.
* `/src/`: Python scripts for mathematical modeling, including:
  * `mle_incubation.py`: Interval-censored MLE for the incubation period.
  * `infectiousness_profile.py`: Generation time deconvolution.
  * `estimate_r0.py`: Negative binomial regression of the offspring distribution.
  * `sim_extinction.py`: 50,000-iteration branching process simulation.
* `/docs/`: Drafts and final versions of the rapid communication manuscript.
* `/figures/`: High-resolution, publication-ready figures mapping the modeled dynamics.

## Usage
All analysis scripts are written in Python 3. Core dependencies include `pandas`, `numpy`, `scipy`, and `matplotlib`.

## Authors
Jason R. Andrews, MD (Stanford University)  
Isaac I. Bogoch, MD (University of Toronto)
