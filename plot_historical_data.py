import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import re
import os

def main():
    data_path = "/Users/jasonandrews/repos/hanta/data/epuyen_2018_cases.csv"
    walkthrough_path = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts/walkthrough.md"
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    
    df = pd.read_csv(data_path)
    df['date_of_onset'] = pd.to_datetime(df['date_of_onset'])
    
    plt.figure(figsize=(12, 6))
    
    # Plot epi curve colored by generation
    sns.histplot(data=df, x='date_of_onset', hue='generation', multiple='stack', palette='viridis', bins=15)
    plt.title('Historical Data: 2018-2019 Epuyén Outbreak Epi Curve (Simulated from Literature)', fontsize=14, fontweight='bold')
    plt.xlabel('Date of Onset', fontsize=12)
    plt.ylabel('Number of Cases', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    timestamp = int(time.time())
    hist_plot_filename = f"historical_epuyen_curve_{timestamp}.png"
    hist_plot_path = os.path.join(artifacts_dir, hist_plot_filename)
    plt.savefig(hist_plot_path, dpi=300)
    plt.close()
    print(f"Saved historical epi curve plot to {hist_plot_path}")
    
    # Update markdown
    with open(walkthrough_path, 'r') as f:
        md_content = f.read()

    if 'Historical Epuyén Data' not in md_content:
        new_md = "\n\n## Historical Epuyén Data (2018-2019)\n"
        new_md += "Based on parameters extracted from the literature (NEJM 2020), this is the modeled epidemiological curve of the Epuyén outbreak, structured by transmission generation.\n\n"
        new_md += f"![Historical Epi Curve]({hist_plot_path})\n"
        md_content += new_md
    else:
        md_content = re.sub(r'(!\[Historical Epi Curve\]\()[^\)]+(\))', rf'\g<1>{hist_plot_path}\g<2>', md_content)

    with open(walkthrough_path, 'w') as f:
        f.write(md_content)
    print(f"Updated {walkthrough_path} with historical plot reference.")

if __name__ == "__main__":
    main()
