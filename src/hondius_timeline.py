import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
from datetime import datetime, timedelta
import os
import time

def main():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 1. Timeline Events (Real Data from WHO)
    events = [
        (datetime(2026, 4, 1), "Cruise Departure\n(Ushuaia, Argentina)"),
        (datetime(2026, 4, 24), "Disembarkation\n(St. Helena)"),
        (datetime(2026, 5, 2), "WHO Notified\n(2 Deaths, 1 Critical)"),
        (datetime(2026, 5, 6), "Disembarkation\n(Praia)"),
        (datetime(2026, 5, 10), "Disembarkation\n(Tenerife)"),
        (datetime(2026, 5, 13), "Repatriation\n(France case symptomatic)"),
    ]
    
    # Base configuration
    ax.set_ylim(0, 10)
    
    # 2. Add specific dates to the timeline
    for i, (date, label) in enumerate(events):
        y_pos = 1 if i % 2 == 0 else 2  # stagger labels
        ax.axvline(date, color='gray', linestyle='--', alpha=0.5, zorder=1)
        ax.plot(date, 3, 'v', color='black', markersize=10, zorder=3)
        ax.text(date, 3.2 + (y_pos*0.5), label, rotation=0, ha='center', va='bottom', 
                fontsize=11, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # 3. Model the epidemiological dynamics based on the data
    
    # Cohort 1: Primary Cases (Infected in Ushuaia, Died by May 2)
    # Exposed ~April 1. Incubation ~20 days. Onset ~April 21. Death ~May 1.
    c1_exp = datetime(2026, 4, 1)
    c1_onset = c1_exp + timedelta(days=20)
    c1_presymp = c1_onset - timedelta(days=4)
    c1_death = datetime(2026, 5, 1)
    
    ax.barh(8, (c1_onset - c1_exp).days, left=c1_exp, height=0.6, color='lightgray', edgecolor='gray', alpha=0.8)
    ax.barh(8, (c1_onset - c1_presymp).days, left=c1_presymp, height=0.6, color='lightcoral', edgecolor='darkred')
    ax.plot(c1_onset, 8, 'ko', markersize=10, markeredgecolor='white', markeredgewidth=1.5)
    ax.plot(c1_death, 8, 'kX', markersize=12, label='Date of Death')
    ax.text(c1_exp - timedelta(days=1), 8, "Primary Cluster\n(2 Deaths)", ha='right', va='center', fontweight='bold')
    
    # Cohort 2: Secondary Cases (The France Repatriated Case)
    # Exposed during Cohort 1's presymptomatic window (April 17-21).
    # Incubation ~20 days. Onset ~May 11 (fits exactly with "symptomatic during repatriation on May 13")
    c2_exp = c1_presymp + timedelta(days=2) # April 19
    c2_onset = datetime(2026, 5, 12)
    c2_presymp = c2_onset - timedelta(days=4)
    
    ax.plot(c2_exp, 6, 'X', color='darkred', markersize=12) # Exposure event
    ax.plot([c2_exp, c2_exp], [6, 8], color='darkred', linestyle=':', alpha=0.5) # Connect transmission
    
    ax.barh(6, (c2_onset - c2_exp).days, left=c2_exp, height=0.6, color='lightgray', edgecolor='gray', alpha=0.8)
    ax.barh(6, 4, left=c2_presymp, height=0.6, color='lightcoral', edgecolor='darkred')
    ax.plot(c2_onset, 6, 'ko', markersize=10, markeredgecolor='white', markeredgewidth=1.5)
    ax.text(c2_exp - timedelta(days=1), 6, "Secondary Cluster\n(e.g., France Case)", ha='right', va='center', fontweight='bold')

    # Cohort 3: Tertiary Risk (Exposed by Cohort 2)
    # Exposed around May 8-12. Need 45 day observation.
    c3_exp = c2_presymp + timedelta(days=2) # May 10
    c3_end_obs = c3_exp + timedelta(days=45)
    
    ax.plot(c3_exp, 4, 'X', color='darkred', markersize=12)
    ax.plot([c3_exp, c3_exp], [4, 6], color='darkred', linestyle=':', alpha=0.5)
    
    ax.barh(4, 45, left=c3_exp, height=0.6, color='khaki', edgecolor='olive', alpha=0.5, hatch='//')
    ax.text(c3_exp - timedelta(days=1), 4, "Tertiary Risk Cohort\n(Requires 45d Monitoring)", ha='right', va='center', fontweight='bold')
    
    # 4. Standard 14-day Quarantine Line (If started at May 2 WHO Notification)
    quar_start = datetime(2026, 5, 2)
    quar_end = quar_start + timedelta(days=14)
    ax.axvspan(quar_start, quar_end, color='orange', alpha=0.1, zorder=0)
    ax.axvline(quar_end, color='darkorange', linestyle='--', linewidth=2.5)
    ax.text(quar_end + timedelta(days=1), 9, "Standard 14-Day\nQuarantine Ends", color='darkorange', fontweight='bold', va='center')
    
    # Create custom legend
    from matplotlib.lines import Line2D
    custom_lines = [
        patches.Rectangle((0,0),1,1, facecolor='lightgray', edgecolor='gray'),
        patches.Rectangle((0,0),1,1, facecolor='lightcoral', edgecolor='darkred'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10),
        Line2D([0], [0], marker='X', color='w', markerfacecolor='black', markersize=12),
        Line2D([0], [0], marker='X', color='w', markerfacecolor='darkred', markersize=12),
        patches.Rectangle((0,0),1,1, facecolor='khaki', edgecolor='olive', hatch='//')
    ]
    ax.legend(custom_lines, ['Silent Incubation Period', 'Presymptomatic Viral Shedding', 'Symptom Onset', 'Date of Death', 'Transmission Exposure Event', 'Required 45-Day Observation Window'], loc='lower left', fontsize=11, bbox_to_anchor=(0, -0.2), ncol=3)

    # Format X axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=45, ha='right', fontsize=12)
    
    ax.set_yticks([])
    ax.set_title('Epidemiological Timeline of the MV Hondius Andes Virus Outbreak', fontsize=16, fontweight='bold', pad=20)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', linestyle='-', alpha=0.2)
    
    # Draw horizontal baseline for events
    ax.axhline(3, color='black', linewidth=1.5, zorder=2)
    
    plt.tight_layout()
    
    artifacts_dir = "/Users/jasonandrews/.gemini/antigravity/brain/26e83a96-4a63-4226-94fe-627b326b4048/artifacts"
    timestamp = int(time.time())
    plot_path = os.path.join(artifacts_dir, f"hondius_timeline_{timestamp}.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved Hondius Timeline to {plot_path}")

if __name__ == "__main__":
    main()
