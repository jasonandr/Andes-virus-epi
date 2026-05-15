import pandas as pd
import numpy as np

def main():
    df = pd.read_csv('/Users/jasonandrews/repos/hanta/data/el_bolson_1996_cases.csv')
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
    
    print(f"El Bolsón 1996 - Serial Interval Analysis:")
    print(f"Number of pairs: {len(serial_intervals)}")
    print(f"Serial Intervals (days): {serial_intervals}")
    print(f"Mean SI: {np.mean(serial_intervals):.2f} days")
    print(f"Median SI: {np.median(serial_intervals):.2f} days")
    print(f"Range SI: {np.min(serial_intervals)} to {np.max(serial_intervals)} days")

if __name__ == "__main__":
    main()
