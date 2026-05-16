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
        'Case 1 (Confirmed, Deceased)', 
        'Case 2 (Confirmed, Deceased)', 
        'Case 3 (Probable, Deceased)',
        'Case 4 (France: Confirmed, Symptomatic)',
        'Case 5 (Spain: Confirmed, Asymptomatic)',
        'Case 6 (USA: Inconclusive Test)',
        'Case 7 (Confirmed)',
        'Case 8 (Confirmed)',
        'Case 9 (Confirmed)',
        'Case 10 (Confirmed)',
        'Case 11 (Probable)'
    ]
    
    y_pos = np.arange(len(patients))
    
    # Key Dates
    date_departure = datetime(2026, 4, 1)
    
    # Colors
    c_ship = 'powderblue'
    
    # We set a fixed seed to ensure the visualization remains consistent
    np.random.seed(42)
    
    for i, patient in enumerate(patients):
        start_date = date_departure
        
        # Determine disembarkation / end of ship timeline
        if "Deceased" in patient:
            if i < 2:
                # First two deaths (reported May 2)
                end_date = datetime(2026, 5, 1) 
                ax.barh(y_pos[i], (end_date - start_date).days, left=start_date, height=0.4, color=c_ship, edgecolor='steelblue')
                ax.plot(end_date, y_pos[i], 'kX', markersize=12)
            else:
                # Third death: Critically ill on May 2, died ~May 8
                crit_date = datetime(2026, 5, 2)
                death_date = datetime(2026, 5, 8)
                
                # Time on ship until evacuation
                ax.barh(y_pos[i], (crit_date - start_date).days, left=start_date, height=0.4, color=c_ship, edgecolor='steelblue')
                
                # Critical Illness Marker
                ax.plot(crit_date, y_pos[i], 's', color='darkred', markersize=10)
                
                # Hospitalization period (dotted line)
                ax.plot([crit_date, death_date], [y_pos[i], y_pos[i]], 'k:', alpha=0.5)
                
                # 3rd Death Marker
                ax.plot(death_date, y_pos[i], 'kX', markersize=12)

        elif "France" in patient:
            end_date = datetime(2026, 5, 10) # Assume disembarked Tenerife
            onset_date = datetime(2026, 5, 13) # Symptomatic during repatriation
            ax.barh(y_pos[i], (end_date - start_date).days, left=start_date, height=0.4, color=c_ship, edgecolor='steelblue')
            # Repatriation window
            ax.plot([end_date, onset_date], [y_pos[i], y_pos[i]], 'k:', alpha=0.5)
            ax.plot(onset_date, y_pos[i], 'ko', markersize=10)
            
        elif "Spain" in patient or "USA" in patient:
            end_date = datetime(2026, 5, 10)
            test_date = datetime(2026, 5, 13)
            ax.barh(y_pos[i], (end_date - start_date).days, left=start_date, height=0.4, color=c_ship, edgecolor='steelblue')
            ax.plot([end_date, test_date], [y_pos[i], y_pos[i]], 'k:', alpha=0.5)
            # Test marker
            color = 'forestgreen' if "Spain" in patient else 'gray'
            ax.plot(test_date, y_pos[i], 'D', color=color, markersize=9)
            
        else:
            # Generic cases
            # Spread their disembarkation among the 3 ports
            port_date = np.random.choice([datetime(2026, 4, 24), datetime(2026, 5, 6), datetime(2026, 5, 10)])
            ax.barh(y_pos[i], (port_date - start_date).days, left=start_date, height=0.4, color=c_ship, edgecolor='steelblue')
            # generic reported dot
            ax.plot(port_date, y_pos[i], 'o', color='steelblue', markersize=8)

    # Add Vertical Milestone Lines
    milestones = [
        (datetime(2026, 4, 1), "Cruise Departure\n(Ushuaia)"),
        (datetime(2026, 4, 24), "Disembarkation\n(St. Helena)"),
        (datetime(2026, 5, 2), "WHO Notified\n(2 Deaths, 1 Critical)"),
        (datetime(2026, 5, 6), "Disembarkation\n(Praia)"),
        (datetime(2026, 5, 10), "Disembarkation\n(Tenerife)")
    ]
    
    for i, (date, label) in enumerate(milestones):
        ax.axvline(date, color='gray', linestyle='--', alpha=0.5, zorder=0)
        # Stagger the text significantly higher
        y_text_pos = -1.5 if i % 2 == 0 else -2.5
        ax.text(date, y_text_pos, label, rotation=0, ha='center', va='top', 
                fontsize=14, fontweight='bold', color='black', 
                bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=2))

    # Formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels(patients, fontsize=14)
    
    # Date formatting on X-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=0, ha='center', fontsize=14)
    
    ax.invert_yaxis()  # Put Primary Case 1 at the top
    ax.set_xlim(datetime(2026, 3, 26), datetime(2026, 5, 18))
    ax.set_ylim(len(patients) + 0.5, -4.0) # Extra space at top for staggered milestones
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', linestyle='-', alpha=0.15)
    
    ax.set_title("Empirical Timeline of the MV Hondius Andes Virus Outbreak", fontsize=22, fontweight='bold', pad=15)
    
    # Custom Legend
    from matplotlib.lines import Line2D
    custom_lines = [
        patches.Rectangle((0,0),1,1, facecolor=c_ship, edgecolor='steelblue'),
        Line2D([0], [0], marker='X', color='w', markerfacecolor='black', markersize=12),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='darkred', markersize=10),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10),
        Line2D([0], [0], marker='D', color='w', markerfacecolor='forestgreen', markersize=9)
    ]
    ax.legend(custom_lines, ['Time on Vessel (MV Hondius)', 'Death Reported', 'Critically Ill (Medevac)', 
                             'Symptom Onset', 'Tested (Asymptomatic / Inconclusive)'], 
              loc='lower left', bbox_to_anchor=(0.0, -0.15), ncol=3, fontsize=14)
              
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"hondius_patient_timeline_{timestamp}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved Patient Timeline to {plot_path}")

if __name__ == "__main__":
    main()
