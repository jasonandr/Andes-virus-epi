import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import time

def main():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Define patients: Index Case + 8 Secondary Cases
    patients = ['Index Case', 'Passenger 1', 'Passenger 2', 'Passenger 3', 
                'Passenger 4', 'Passenger 5', 'Passenger 6', 'Passenger 7', 'Passenger 8']
    
    y_pos = np.arange(len(patients))
    
    # Event timings
    incubation = 20 # median incubation
    presymp_window = 3 # days before onset where highly infectious
    buffet_day = 18 # Index case goes to buffet on day 18 (presymptomatic)
    
    # Colors
    c_incubation = 'lightgray'
    c_presymp = 'lightcoral'
    c_onset = 'black'
    
    for i, patient in enumerate(patients):
        if i == 0:
            # Index case
            start_day = 0
            # Incubation bar
            ax.barh(y_pos[i], incubation, left=start_day, height=0.4, color=c_incubation, edgecolor='gray', alpha=0.8)
            # Presymptomatic bar overlays the last 3 days of incubation
            ax.barh(y_pos[i], presymp_window, left=incubation - presymp_window, height=0.4, color=c_presymp, edgecolor='darkred')
            # Symptom Onset
            ax.plot(incubation, y_pos[i], 'ko', markersize=10, markeredgecolor='white', markeredgewidth=1.5)
            
            # The superspreading event
            ax.plot(buffet_day, y_pos[i], 'X', color='darkred', markersize=12, label='Superspreading Event (Buffet)')
            ax.axvline(x=buffet_day, color='darkred', linestyle=':', alpha=0.5)
            
        else:
            # Secondary cases infected at buffet
            start_day = buffet_day
            # Add some slight variation to their incubation (18-22 days)
            np.random.seed(42 + i)
            ind_incubation = np.random.normal(20.1, 1.5)
            
            # Incubation bar
            ax.barh(y_pos[i], ind_incubation, left=start_day, height=0.4, color=c_incubation, edgecolor='gray', alpha=0.8)
            # Presymptomatic bar overlays the last 3 days of incubation
            ax.barh(y_pos[i], presymp_window, left=start_day + ind_incubation - presymp_window, height=0.4, color=c_presymp, edgecolor='darkred')
            # Symptom Onset
            ax.plot(start_day + ind_incubation, y_pos[i], 'ko', markersize=10, markeredgecolor='white', markeredgewidth=1.5)

    # Standard 14-day Quarantine Line
    ax.axvline(x=14, color='orange', linestyle='--', linewidth=2.5, zorder=0)
    ax.text(14.5, 8.5, "Standard 14-Day\nQuarantine Ends", color='darkorange', fontweight='bold', fontsize=14, va='top')
    
    # Proposed 45-day Quarantine Line
    ax.axvline(x=45, color='forestgreen', linestyle='--', linewidth=2.5, zorder=0)
    ax.text(45.5, 8.5, "Proposed 45-Day\nObservation Ends", color='forestgreen', fontweight='bold', fontsize=14, va='top')
    
    # Create custom legend
    from matplotlib.lines import Line2D
    custom_lines = [
        patches.Rectangle((0,0),1,1, facecolor=c_incubation, edgecolor='gray'),
        patches.Rectangle((0,0),1,1, facecolor=c_presymp, edgecolor='darkred'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10),
        Line2D([0], [0], marker='X', color='w', markerfacecolor='darkred', markersize=12)
    ]
    ax.legend(custom_lines, ['Silent Incubation Period', 'Presymptomatic Viral Shedding', 'Fever / Symptom Onset', 'Superspreading Exposure'], loc='lower right', fontsize=14)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(patients, fontsize=16)
    ax.set_xlabel('Days Since Initial Vessel Exposure', fontsize=17, fontweight='bold')
    ax.set_title('The Danger of Silent Spread: Andes Virus Outbreak Timeline', fontsize=22, fontweight='bold', pad=15)
    
    ax.invert_yaxis()  # Index case at top
    ax.set_xlim(-2, 50)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', linestyle='-', alpha=0.2)
    
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"gantt_plot_{timestamp}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved Gantt plot to {plot_path}")

if __name__ == "__main__":
    main()
