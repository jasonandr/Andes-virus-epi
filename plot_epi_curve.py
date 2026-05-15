import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import re
import os

def main():
    data_path = "/Users/jasonandrews/repos/hanta/data/hondius_cases.csv"
    walkthrough_path = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts/walkthrough.md"
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    
    # Load data
    df = pd.read_csv(data_path)
    df['date_of_onset'] = pd.to_datetime(df['date_of_onset'])
    
    # Plot
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='date_of_onset', hue='status', multiple='stack', bins=10, palette='viridis')
    plt.title('Epi Curve: Hantavirus (Andes) Outbreak on MV Hondius')
    plt.xlabel('Date of Onset')
    plt.ylabel('Number of Cases')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save with cache busting
    timestamp = int(time.time())
    new_plot_filename = f"epi_curve_{timestamp}.png"
    new_plot_path = os.path.join(artifacts_dir, new_plot_filename)
    plt.savefig(new_plot_path)
    print(f"Saved plot to {new_plot_path}")
    
    # Regex subroutine to update markdown
    with open(walkthrough_path, 'r') as f:
        md_content = f.read()
    
    # Regex to find ![Epi Curve](/path/to/epi_curve_*.png)
    pattern = r'(!\[Epi Curve\]\()[^\)]+(\))'
    updated_content = re.sub(pattern, rf'\g<1>{new_plot_path}\g<2>', md_content)
    
    with open(walkthrough_path, 'w') as f:
        f.write(updated_content)
    print(f"Updated {walkthrough_path} with new plot reference.")

if __name__ == "__main__":
    main()
