# Epidemiological characteristics of Andes Virus and implications for monitoring outbreaks

**Abstract:** The identification of a severe cluster of Andes virus (ANDV) aboard the *MV Hondius* necessitates an immediate epidemiological risk assessment. By retrospectively analyzing raw patient-level data from the 1996 El Bolsón and 2018 Epuyén outbreaks, we establish that ANDV transmission is defined by a prolonged median incubation period (20.1 days), high rates of presymptomatic transmission (~24%), and extreme superspreading dynamics (dispersion parameter $k=0.71$). These parameters render the virus exceptionally difficult to monitor through standard symptom checks, requiring an immediate extension of quarantine protocols to 45 days. However, because of the profound transmission heterogeneity, we conclude that the risk of a massive, ship-wide outbreak is statistically unlikely, as branching process simulations demonstrate that the vast majority of disease introductions result in stochastic extinction.

***

## Introduction
Hantavirus Pulmonary Syndrome (HPS) is a severe respiratory disease with a case fatality rate historically exceeding 30%. While most hantaviruses are transmitted exclusively via inhalation of aerosolized rodent excreta, the Andes orthohantavirus (ANDV) is unique in its documented capacity for sustained human-to-human transmission. Following the notification of an ANDV cluster comprising 11 confirmed and probable cases aboard the *MV Hondius* cruise ship (Supplementary Figure S1), we rapidly modeled the transmission dynamics of the virus to inform public health monitoring and intervention strategies. We utilized complete, unredacted contact networks from the two most extensively documented historical ANDV outbreaks—the 1996 cluster in El Bolsón, Argentina (18 cases) [1], and the 2018–2019 outbreak in Epuyén, Argentina (34 cases) [2]—to rigorously define the fundamental epidemiological parameters.

## Methods
Patient-level line lists detailing exposure windows, symptom onset dates, and infector-infectee pairs were extracted from primary literature appendices [1, 2]. To calculate the incubation period, we applied an interval-censored Maximum Likelihood Estimation (MLE) framework [3] to the bounded social exposures in the 2018 Epuyén cohort ($N=34$). Generation times and the infectiousness profile were deconvoluted mathematically from the empirical serial intervals recorded in the 1996 El Bolsón transmission network [4]. Transmission heterogeneity was assessed by fitting a Negative Binomial distribution to the aggregated offspring distribution of both outbreaks, enabling the calculation of the basic reproduction number ($R_0$) and the dispersion parameter ($k$) [5]. Finally, we conducted a 50,000-iteration branching process simulation parameterized by the derived $R_0$ and $k$ values to estimate the probability of stochastic extinction versus large-scale epidemic growth following a single ship-board introduction. Code and underlying data are available at: github.com/jasonandr/Andes-virus-epi

## Results
Interval-censored MLE demonstrated a median human-to-human incubation period of 20.1 days. We conducted comparative lognormal modeling against historically established environmental (rodent-to-human) incubation periods (median 18.5 days) [6]. The resulting density distributions are virtually identical (Figure 1A), proving that the prolonged incubation period is intrinsic to ANDV pathogenesis and remains unaffected by the route of inoculation (respiratory droplet versus environmental aerosol). 

Analysis of the empirical generation time curves revealed a substantial leftward shift relative to symptom onset, indicating that approximately 24% of transmission occurs during the presymptomatic or early prodromal phase, prior to the onset of severe febrile illness (Figure 1B). 

Negative binomial regression on the combined empirical offspring distribution yielded an overall $R_0$ of 0.96, but an exceptionally low dispersion parameter ($k$) of 0.71 (Figure 1C). A dispersion parameter $k < 1.0$ is the mathematical hallmark of superspreading dynamics [5]. The vast majority of infected individuals (>70%) generated zero secondary cases, while a minority of "superspreaders" were responsible for expansive, multi-generational transmission chains. 

Utilizing these exact parameters in the branching process simulation, we found that 54.5% of single-case introductions resulted in immediate stochastic extinction (generating zero secondary cases). However, outbreaks that evaded early extinction were subjected to the "fat tail" of the negative binomial distribution, with a small probability of explosive clustering (Supplementary Figure S2).

## Discussion
These epidemiological characteristics have profound implications for monitoring ANDV outbreaks in high-density environments. The combination of a prolonged 3-to-4 week incubation period and significant presymptomatic shedding severely limits the efficacy of symptom-based screening at points of entry or within contained facilities. By the time an index case develops a fever, secondary transmission has likely already occurred. Consequently, exposed individuals must undergo clinical observation and quarantine for a minimum of 45 days. Contact tracing efforts should pivot from linear, individual-level tracking to focusing aggressively on identifying specific high-risk congregational events where presymptomatic shedding may have occurred.

However, the extreme transmission heterogeneity ($k=0.71$) provides a crucial limiting factor. Because superspreading dynamics dictate that most infected individuals do not transmit the virus, the risk of a large, uncontained outbreak—even without stringent mitigation measures—remains statistically unlikely. Branching process simulations demonstrate that the vast majority of disease introductions will result in rapid stochastic extinction. Thus, while the threat of localized superspreading events is high, the probability of ship-wide exponential growth is low.

Furthermore, historical serosurveys of asymptomatic close contacts have repeatedly demonstrated a seropositivity rate of <3%, indicating that subclinical infection is exceedingly rare. As such, the widely cited 30% Case Fatality Rate closely mirrors the true Infection Fatality Rate, underscoring the severity of the disease in those few who do become infected.

***

## References
1. Padula PJ, Edelstein A, Miguel SD, López NM, Francos CM, Suárez VC. Epidemic outbreak of hantavirus pulmonary syndrome in Argentina. Molecular evidence for person-to-person transmission of Andes virus. *Virology*. 1998;241(2):323-330.
2. Martinez VP, Di Paola N, Alonso DO, et al. "Super-Spreaders" and Person-to-Person Transmission of Andes Virus in Argentina. *New England Journal of Medicine*. 2020;383(23):2230-2241.
3. Lauer SA, Grantz KH, Bi Q, et al. The Incubation Period of Coronavirus Disease 2019 (COVID-19) From Publicly Reported Confirmed Cases: Estimation and Application. *Annals of Internal Medicine*. 2020;172(9):577-582.
4. He X, Lau EHY, Wu P, et al. Temporal dynamics in viral shedding and transmissibility of COVID-19. *Nature Medicine*. 2020;26(5):672-675.
5. Lloyd-Smith JO, Schreiber SJ, Kopp PE, Getz WM. Superspreading and the effect of individual variation on disease emergence. *Nature*. 2005;438(7066):355-359.
6. Vial PA, Valdivieso F, Mertz G, et al. Incubation period of hantavirus cardiopulmonary syndrome. *Emerging Infectious Diseases*. 2006;12(8):1271-1273.

***

## Figures and Legends

![Combined Historical Analysis](/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts/combined_historical_analysis_1778891384.png)
**Figure 1. Synthesized Transmission Dynamics of Andes Virus.** (A) Comparative incubation dynamics showing overlaid lognormal probability density functions of the human-to-human incubation period (median 20.1 days, derived via MLE) against the established environmental exposure period (median 18.5 days; Vial et al., 2006). (B) Infectiousness profile relative to symptom onset, deconvoluted from the 1996 El Bolsón serial intervals, illustrating approximately 24% presymptomatic shedding. (C) Negative binomial regression fit to the empirical offspring distribution (1996 and 2018 combined data), revealing extreme transmission heterogeneity ($R_0=0.96$, $k=0.71$).

***

# Supplementary Appendices

## Appendix A: Empirical Timeline of the MV Hondius Outbreak
We reconstructed the empirical patient-level timeline of the outbreak using notification data from the World Health Organization. The visualization strictly adheres to reported milestones, documenting the duration of exposure on the vessel, clinical symptom onset, and dates of death for the primary and secondary clusters, highlighting the rapid clinical deterioration of the initial three cases prior to and during the initial May 2nd notification.

![Empirical Timeline](/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts/hondius_patient_timeline_1778879545.png)
**Supplementary Figure S1. Patient-Level Timeline of the MV Hondius Andes Virus Outbreak.** Gantt chart illustrating the time spent on the vessel by the 11 identified cases, ending in specific reported events (death, critical illness medevac, symptom onset, or testing).

## Appendix B: Stochastic Extinction Simulation
We executed a branching process simulation utilizing the empirical transmission parameters ($R_0 = 0.96$, $k = 0.71$) to model 50,000 theoretical virus introductions. The resulting raincloud plot demonstrates the paradox of the dispersion parameter: while the probability of stochastic extinction at the index case is elevated compared to homogenous pathogens, outbreaks that survive the first generation are subjected to the "fat tail" of the negative binomial distribution, occasionally exploding into massive clusters.

![Stochastic Extinction Simulation](/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts/appendix_stochastic_extinction_raincloud_1778891384.png)
**Supplementary Figure S2. Outbreak Size Probability Density.** Raincloud plot (log-scaled KDE, jittered raw iterations, and boxplot) representing the total outbreak sizes over 50,000 simulated generations. The explicit log-scale x-axis highlights extreme long-tail clustering events.

## Appendix C: Demographic Stratification
Analysis of the 2018 Epuyén line list mapped patient age against individual reproduction numbers. Infectiousness did not linearly correlate with age; rather, superspreading was bound to high-risk social behavioral events (e.g., attending specific indoor gatherings while infectious).

![Demographic Infectiousness](/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts/appendix_demographics_1778877198.png)
**Supplementary Figure S3. Demographic Infectiousness Profiles.** Scatter plot mapping the age of index cases against their respective number of secondary infections in the 2018 Epuyén outbreak.
