import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
import time
import re

def main():
    data_path = "/Users/jasonandrews/repos/hanta/data/el_bolson_1996_cases.csv"
    walkthrough_path = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts/walkthrough.md"
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    
    df = pd.read_csv(data_path)
    df['date_of_onset'] = pd.to_datetime(df['date_of_onset'])
    
    # Calculate Serial Intervals
    serial_intervals = []
    for idx, row in df.iterrows():
        infector = row['infector_id']
        if pd.notna(infector) and infector != 'None':
            infector_row = df[df['case_id'] == infector]
            if not infector_row.empty:
                infector_onset = infector_row.iloc[0]['date_of_onset']
                si = (row['date_of_onset'] - infector_onset).days
                serial_intervals.append(si)
                
    serial_intervals = np.array(serial_intervals)
    
    # Fit a Gamma distribution to the empirical serial intervals
    mean_si = np.mean(serial_intervals)
    std_si = np.std(serial_intervals)
    
    shape = (mean_si / std_si) ** 2
    scale = (std_si ** 2) / mean_si
    
    # He et al. Methodology: 
    # Infectiousness profile relative to symptom onset.
    # In a simplified approach, if Generation Time ~ Serial Interval,
    # the time of transmission relative to symptom onset = Generation Time - Incubation Period.
    # We use the literature median incubation period of 18 days.
    incubation_period = 18
    
    x_generation = np.linspace(0, 50, 500)
    pdf_generation = stats.gamma.pdf(x_generation, a=shape, scale=scale)
    
    # Shift x-axis by incubation period to get "days relative to symptom onset"
    x_relative = x_generation - incubation_period
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_relative, pdf_generation, color='darkred', linewidth=3, label='Infectiousness Profile')
    plt.fill_between(x_relative, pdf_generation, alpha=0.3, color='darkred')
    
    # Add vertical line for symptom onset
    plt.axvline(x=0, color='black', linestyle='--', linewidth=2, label='Symptom Onset')
    
    # Calculate presymptomatic vs symptomatic proportion
    presymp_prob = stats.gamma.cdf(incubation_period, a=shape, scale=scale)
    
    plt.title('B', loc='left', fontsize=22, fontweight='bold')
    plt.xlabel('Days Relative to Symptom Onset', fontsize=16)
    plt.ylabel('Relative Infectiousness', fontsize=16)
    
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    timestamp = int(time.time())
    infect_plot_filename = f"infectiousness_profile_{timestamp}.png"
    infect_plot_path = os.path.join(artifacts_dir, infect_plot_filename)
    plt.savefig(infect_plot_path, dpi=300)
    plt.close()
    
    print(f"Saved infectiousness profile plot to {infect_plot_path}")
    
    # Update markdown Walkthrough
    with open(walkthrough_path, 'r') as f:
        md_content = f.read()

    if 'Infectiousness Profile' not in md_content:
        new_md = "\n\n## Infectiousness Profile (He et al. Methodology)\n"
        new_md += "Using the empirical serial intervals from the 1996 El Bolsón outbreak, we inferred the infectiousness profile relative to symptom onset. By shifting the fitted Gamma distribution by the known median incubation period (18 days), we can visualize the window of highest transmissibility, including potential presymptomatic spread.\n\n"
        new_md += f"![Infectiousness Profile]({infect_plot_path})\n"
        md_content += new_md
    else:
        md_content = re.sub(r'(!\[Infectiousness Profile\]\()[^\)]+(\))', rf'\g<1>{infect_plot_path}\g<2>', md_content)

    with open(walkthrough_path, 'w') as f:
        f.write(md_content)

if __name__ == "__main__":
    main()
