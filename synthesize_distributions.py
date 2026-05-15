import json
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import time
import re
import os

def main():
    with open('/Users/jasonandrews/repos/hanta/data/andes_extracted_parameters.json', 'r') as f:
        params = json.load(f)

    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    walkthrough_path = os.path.join(artifacts_dir, "walkthrough.md")

    # We will model the Incubation Period as a Lognormal distribution
    # Median = 18 days. 95% CI roughly within the range [4, 42].
    # For lognormal, median = exp(mu). So mu = ln(18) ~ 2.89
    mu_inc = np.log(params['incubation_period']['median_days'])
    
    # We calibrate sigma so that the 99th percentile is around 42 days.
    # ln(42) = mu + 2.326 * sigma -> sigma = (ln(42) - 2.89) / 2.326 ~ 0.36
    sigma_inc = (np.log(42) - mu_inc) / 2.326
    
    x = np.linspace(0, 60, 500)
    pdf_inc = stats.lognorm.pdf(x, s=sigma_inc, scale=np.exp(mu_inc))

    # We model the Serial Interval as a Gamma distribution
    # Range is 19 to 40 days, let's assume a mean of ~26 days
    mean_si = 26
    # Assume 95% of data is between 15 and 40. Standard dev ~ 6
    std_si = 6
    shape_si = (mean_si / std_si)**2
    scale_si = (std_si**2) / mean_si
    
    pdf_si = stats.gamma.pdf(x, a=shape_si, scale=scale_si)

    plt.figure(figsize=(12, 6))
    
    plt.plot(x, pdf_inc, label='Incubation Period (Lognormal)', color='blue', linewidth=2.5)
    plt.fill_between(x, pdf_inc, alpha=0.3, color='blue')
    
    plt.plot(x, pdf_si, label='Serial Interval (Gamma)', color='orange', linewidth=2.5)
    plt.fill_between(x, pdf_si, alpha=0.3, color='orange')
    
    # Highlight extracted ranges
    plt.axvspan(params['incubation_period']['range_days'][0], params['incubation_period']['range_days'][1], 
                color='blue', alpha=0.1, ymin=0, ymax=0.1, label='Extracted Incubation Range (4-42)')
    plt.axvspan(params['serial_interval']['range_days'][0], params['serial_interval']['range_days'][1], 
                color='orange', alpha=0.1, ymin=0.1, ymax=0.2, label='Extracted Serial Interval Range (19-40)')

    plt.title('A. Foundational Parameter Distributions', fontsize=14, fontweight='bold')
    plt.xlabel('Days', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(alpha=0.4)
    plt.tight_layout()

    # Cache busting save
    timestamp = int(time.time())
    dist_plot_filename = f"parameter_distributions_{timestamp}.png"
    dist_plot_path = os.path.join(artifacts_dir, dist_plot_filename)
    plt.savefig(dist_plot_path, dpi=300)
    plt.close()
    
    # Update markdown
    with open(walkthrough_path, 'r') as f:
        md_content = f.read()

    if 'Statistical Parameter Synthesis' not in md_content:
        new_md = "\n\n## Statistical Parameter Synthesis\n"
        new_md += "Using extracted historical literature data, we synthesized probability density functions for the incubation period and serial interval.\n\n"
        new_md += f"![Parameter Distributions]({dist_plot_path})\n"
        md_content += new_md
    else:
        md_content = re.sub(r'(!\[Parameter Distributions\]\()[^\)]+(\))', rf'\g<1>{dist_plot_path}\g<2>', md_content)

    with open(walkthrough_path, 'w') as f:
        f.write(md_content)
    
    print(f"Generated statistical synthesis plot and updated Walkthrough.")

if __name__ == "__main__":
    main()
