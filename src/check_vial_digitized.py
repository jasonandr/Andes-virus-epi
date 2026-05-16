import pandas as pd
import numpy as np

df = pd.read_csv('/Users/jasonandrews/repos/hanta/data/vial_2006_digitized_figure1.csv')

# Calculate potential incubation range for each patient
df['max_incubation'] = df['symptom_onset_days'] - df['exposure_start_days']
df['min_incubation'] = df['symptom_onset_days']

print("All patients (n=20):")
print(f"Global Minimum Incubation: {df['min_incubation'].min()}")
print(f"Global Maximum Incubation: {df['max_incubation'].max()}")

# How to compute the "median incubation" of 18 days?
# The paper says: "The potential maximum incubation period for all 20 patients was 11-39 days, and the potential minimum incubation period was 7-32 days. The median incubation period for all 20 patients was 18 days (range 7-39 days)."
# Median of what? Maybe the midpoint of min and max? Or median of min? Or median of max?
df['mid_incubation'] = (df['min_incubation'] + df['max_incubation']) / 2
print(f"Median of min incubation: {df['min_incubation'].median()}")
print(f"Median of max incubation: {df['max_incubation'].median()}")
print(f"Median of mid incubation: {df['mid_incubation'].median()}")

# Short exposure patients (exposure < 48 hours)
# These are patients 10 to 20
df_short = df[df['patient_id'] >= 10]
print("\nShort exposure patients (n=11):")
print(f"Global Minimum Incubation: {df_short['min_incubation'].min()}")
print(f"Global Maximum Incubation: {df_short['max_incubation'].max()}")
print(f"Median of min incubation: {df_short['min_incubation'].median()}")
print(f"Median of max incubation: {df_short['max_incubation'].median()}")
print(f"Median of mid incubation: {df_short['mid_incubation'].median()}")

