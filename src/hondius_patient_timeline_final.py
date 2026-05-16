import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
from datetime import datetime, timedelta
import numpy as np
import os
import time

def main():
    fig, ax = plt.subplots(figsize=(16, 10))
    
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
    date_departure = datetime(2026, 4, 1)
    
    np.random.seed(42)
    
    for i, patient in enumerate(patients):
        
        # We will draw a very faint thin baseline for each patient so the icons aren't floating in nowhere
        ax.axhline(y=y_pos[i], color='gray', linestyle=':', alpha=0.2, zorder=0)

        if i < 3:
            # Primary Cases
            # Estimated onset based on death date
            if i < 2:
                death_date = datetime(2026, 5, 1)
                onset_date = death_date - timedelta(days=10)
                
                ax.plot(onset_date, y_pos[i], 'ko', markersize=9, markeredgecolor='white', markeredgewidth=1)
                ax.plot(death_date, y_pos[i], 'kX', markersize=11)
                ax.plot([onset_date, death_date], [y_pos[i], y_pos[i]], 'k-', linewidth=1, alpha=0.5)
            else:
                # Third death: Critically ill on May 2, died ~May 8
                crit_date = datetime(2026, 5, 2)
                death_date = datetime(2026, 5, 8)
                onset_date = crit_date - timedelta(days=6)
                
                ax.plot(onset_date, y_pos[i], 'ko', markersize=9, markeredgecolor='white', markeredgewidth=1)
                ax.plot([onset_date, crit_date], [y_pos[i], y_pos[i]], 'k-', linewidth=1, alpha=0.5)
                
                # Critical Illness Marker
                ax.plot(crit_date, y_pos[i], 's', color='darkred', markersize=10)
                
                # Hospitalization to death
                ax.plot([crit_date, death_date], [y_pos[i], y_pos[i]], 'k:', alpha=0.5)
                ax.plot(death_date, y_pos[i], 'kX', markersize=12)

        else:
            # Secondary Cases 
            if "France" in patient:
                onset_date = datetime(2026, 5, 13)
                ax.plot(onset_date, y_pos[i], 'ko', markersize=9, markeredgecolor='white', markeredgewidth=1)
            elif "Spain" in patient:
                test_date = datetime(2026, 5, 13)
                ax.plot(test_date, y_pos[i], 'D', color='forestgreen', markersize=9)
            elif "USA" in patient:
                test_date = datetime(2026, 5, 13)
                ax.plot(test_date, y_pos[i], 'D', color='gray', markersize=9)
            else:
                # Generic cases: just place a dot around when they were reported
                report_date = np.random.choice([datetime(2026, 5, 6), datetime(2026, 5, 10)])
                ax.plot(report_date, y_pos[i], 'o', color='steelblue', markersize=8)

    # Add Vertical Milestone Lines (From Version 4)
    milestones = [
        (datetime(2026, 4, 1), "Cruise Departure\n(Ushuaia)"),
        (datetime(2026, 4, 24), "Disembarkation\n(St. Helena)"),
        (datetime(2026, 5, 2), "WHO Notified\n(2 Deaths, 1 Critical)"),
        (datetime(2026, 5, 6), "Disembarkation\n(Praia)"),
        (datetime(2026, 5, 10), "Disembarkation\n(Tenerife)")
    ]
    
    for i, (date, label) in enumerate(milestones):
        ax.axvline(date, color='steelblue', linestyle='--', alpha=0.6, zorder=0)
        y_text_pos = -1.5 if i % 2 == 0 else -2.5
        ax.text(date, y_text_pos, label, rotation=0, ha='center', va='top', 
                fontsize=14, fontweight='bold', color='steelblue', 
                bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=2))

    # Formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels(patients, fontsize=14)
    
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=0, ha='center', fontsize=14)
    
    ax.invert_yaxis()
    ax.set_xlim(datetime(2026, 3, 26), datetime(2026, 5, 20))
    ax.set_ylim(len(patients) + 0.5, -4.0)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    ax.set_title("", fontsize=22, fontweight='bold', pad=15)
    
    # Custom Legend
    from matplotlib.lines import Line2D
    custom_lines = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='darkred', markersize=10),
        Line2D([0], [0], marker='X', color='w', markerfacecolor='black', markersize=11),
        Line2D([0], [0], marker='D', color='w', markerfacecolor='forestgreen', markersize=9),
        Line2D([0], [0], marker='D', color='w', markerfacecolor='gray', markersize=9),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='steelblue', markersize=8)
    ]
    ax.legend(custom_lines, ['Symptom Onset', 'Critically Ill (Medevac)', 'Date of Death', 'Tested Asymptomatic', 'Inconclusive Test', 'Case Confirmed / Reported'], 
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
