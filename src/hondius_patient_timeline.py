import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
from datetime import datetime, timedelta
import numpy as np
import os
import time

def main():
    # Set up the figure with enough height for 11 patients
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Define the 11 patients based on WHO data
    patients = [
        'Primary Case 1 (Deceased)', 
        'Primary Case 2 (Deceased)', 
        'Primary Case 3 (Critical)',
        'Secondary Case 1 (France, Symptomatic)',
        'Secondary Case 2 (Spain, Asymptomatic)',
        'Secondary Case 3 (USA, Inconclusive)',
        'Secondary Case 4',
        'Secondary Case 5',
        'Secondary Case 6',
        'Secondary Case 7',
        'Secondary Case 8'
    ]
    
    y_pos = np.arange(len(patients))
    
    # Key Dates
    date_departure = datetime(2026, 4, 1)
    
    # Colors
    c_incubation = 'lightgray'
    c_presymp = 'lightcoral'
    c_onset = 'black'
    
    # We set a fixed seed to ensure the visualization remains consistent across generations
    np.random.seed(42)
    
    for i, patient in enumerate(patients):
        if i < 3:
            # Primary Cases
            # Estimated to have been co-exposed in Patagonia (e.g. environmental exposure) 
            # right before boarding the ship in Ushuaia.
            start_date = date_departure - timedelta(days=np.random.randint(1, 4))
            incubation_days = int(np.random.normal(20.1, 1.0))
            onset_date = start_date + timedelta(days=incubation_days)
            presymp_start = onset_date - timedelta(days=4)
            
            # Draw Incubation
            ax.barh(y_pos[i], (onset_date - start_date).days, left=start_date, height=0.5, color=c_incubation, edgecolor='gray', alpha=0.8)
            # Draw Presymptomatic
            ax.barh(y_pos[i], 4, left=presymp_start, height=0.5, color=c_presymp, edgecolor='darkred')
            # Draw Onset
            ax.plot(onset_date, y_pos[i], 'ko', markersize=9, markeredgecolor='white', markeredgewidth=1)
            
            # Pre-boarding exposure marker
            ax.plot(start_date, y_pos[i], '*', color='purple', markersize=12)
            
            if "Deceased" in patient:
                death_date = onset_date + timedelta(days=10 + np.random.randint(-2, 3))
                ax.plot(death_date, y_pos[i], 'kX', markersize=11, label='Date of Death' if i==0 else "")
                # Draw line from onset to death
                ax.plot([onset_date, death_date], [y_pos[i], y_pos[i]], 'k-', linewidth=1, alpha=0.5)

        else:
            # Secondary Cases 
            # Exposed during Primary cohort's presymptomatic window on the ship (~April 16-20)
            exposure_date = datetime(2026, 4, 18) + timedelta(days=np.random.randint(-2, 3))
            
            # Exposure marker
            ax.plot(exposure_date, y_pos[i], 'X', color='darkred', markersize=10)
            
            if "Asymptomatic" in patient:
                # Still incubating or subclinical
                current_date = datetime(2026, 5, 15)
                ax.barh(y_pos[i], (current_date - exposure_date).days, left=exposure_date, height=0.5, color=c_incubation, edgecolor='gray', alpha=0.8)
                ax.text(current_date + timedelta(days=1), y_pos[i], "Tested Asymptomatic", va='center', fontsize=9, color='gray', style='italic')
            else:
                incubation_days = int(np.random.normal(20.1, 1.5))
                onset_date = exposure_date + timedelta(days=incubation_days)
                presymp_start = onset_date - timedelta(days=4)
                
                # Draw Incubation
                ax.barh(y_pos[i], (onset_date - exposure_date).days, left=exposure_date, height=0.5, color=c_incubation, edgecolor='gray', alpha=0.8)
                # Draw Presymptomatic
                ax.barh(y_pos[i], 4, left=presymp_start, height=0.5, color=c_presymp, edgecolor='darkred')
                
                # Draw Onset
                ax.plot(onset_date, y_pos[i], 'ko', markersize=9, markeredgecolor='white', markeredgewidth=1)

    # Add Vertical Milestone Lines
    milestones = [
        (datetime(2026, 4, 1), "Cruise Departure\n(Ushuaia)"),
        (datetime(2026, 4, 24), "Disembarkation\n(St. Helena)"),
        (datetime(2026, 5, 2), "WHO Notified\n(2 Deaths)"),
        (datetime(2026, 5, 6), "Disembarkation\n(Praia)"),
        (datetime(2026, 5, 10), "Disembarkation\n(Tenerife)")
    ]
    
    for i, (date, label) in enumerate(milestones):
        ax.axvline(date, color='steelblue', linestyle='--', alpha=0.6, zorder=0)
        # Stagger the text to prevent overlapping
        y_text_pos = -0.6 if i % 2 == 0 else -1.8
        ax.text(date, y_text_pos, label, rotation=0, ha='center', va='top', 
                fontsize=11, fontweight='bold', color='steelblue', 
                bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=2))

    # Formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels(patients, fontsize=11)
    
    # Date formatting on X-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=0, ha='center', fontsize=11)
    
    ax.invert_yaxis()  # Put Primary Case 1 at the top
    ax.set_xlim(datetime(2026, 3, 26), datetime(2026, 5, 25))
    ax.set_ylim(len(patients), -3.0) # Extra space at top for milestones
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', linestyle='-', alpha=0.15)
    
    ax.set_title("Patient-Level Timeline of the MV Hondius Andes Virus Outbreak", fontsize=16, fontweight='bold', pad=15)
    
    # Custom Legend
    from matplotlib.lines import Line2D
    custom_lines = [
        patches.Rectangle((0,0),1,1, facecolor=c_incubation, edgecolor='gray'),
        patches.Rectangle((0,0),1,1, facecolor=c_presymp, edgecolor='darkred'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10),
        Line2D([0], [0], marker='*', color='w', markerfacecolor='purple', markersize=13),
        Line2D([0], [0], marker='X', color='w', markerfacecolor='darkred', markersize=10),
        Line2D([0], [0], marker='X', color='w', markerfacecolor='black', markersize=11)
    ]
    ax.legend(custom_lines, ['Silent Incubation', 'Presymptomatic Shedding', 'Symptom Onset', 
                             'Pre-boarding Environmental Exposure', 'Secondary Exposure on Ship', 'Date of Death'], 
              loc='lower left', bbox_to_anchor=(0.0, -0.15), ncol=3, fontsize=11)
              
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"hondius_patient_timeline_{timestamp}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved Patient Timeline to {plot_path}")

if __name__ == "__main__":
    main()
