import pdfplumber
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
import numpy as np

def main():
    pdf_path = "/Users/jasonandrews/repos/hanta/literature/nejmoa2009040_appendix_1.pdf"
    
    patients = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split('\n'):
                    if line.startswith("Patient"):
                        parts = line.split()
                        try:
                            patient_id = parts[1]
                            age = float(parts[2])
                            sex = parts[3]
                            
                            # Find onset date
                            dates = re.findall(r'\d{1,2}/\d{1,2}/\d{4}', line)
                            if len(dates) >= 1:
                                onset_date = dates[-1]
                                onset_idx = parts.index(onset_date)
                                infector_str = parts[onset_idx + 1]
                                
                                if infector_str.isdigit():
                                    infector_id = infector_str
                                else:
                                    infector_id = None
                                    
                                patients[patient_id] = {
                                    'age': age,
                                    'sex': sex,
                                    'infector': infector_id,
                                    'secondary_cases': 0
                                }
                        except Exception:
                            continue
                            
    # Count secondary cases
    for pat_id, data in patients.items():
        inf = data['infector']
        if inf and inf in patients:
            patients[inf]['secondary_cases'] += 1
            
    df = pd.DataFrame.from_dict(patients, orient='index')
    
    plt.figure(figsize=(7, 5))
    
    # Age vs Secondary Cases
    sns.scatterplot(data=df, x='age', y='secondary_cases', hue='sex', s=100, alpha=0.7, palette='Set1')
    
    # Add a slight jitter for overlapping points
    np.random.seed(42)
    jitter_y = df['secondary_cases'] + np.random.normal(0, 0.1, len(df))
    plt.scatter(df['age'], jitter_y, alpha=0) # invisible just for scale
    
    plt.title('Age vs. Infectiousness (2018 Epuyén)', fontweight='bold')
    plt.xlabel('Age (Years)')
    plt.ylabel('Number of Secondary Cases')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"appendix_demographics_{timestamp}.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    
    print(f"Saved demographic infectiousness to {plot_path}")

if __name__ == "__main__":
    main()
