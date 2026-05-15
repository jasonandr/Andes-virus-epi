import pandas as pd
import numpy as np
from datetime import timedelta, datetime

def generate_epuyen_data():
    """
    Generates a synthetic line list for the 2018-2019 Epuyén Andes virus outbreak
    based on published parameters (NEJM 2020):
    - 34 total confirmed cases
    - 11 deaths (32% CFR)
    - Single zoonotic index case
    - R0 ~ 2.1
    - Incubation period 9 to 40 days
    """
    np.random.seed(42)
    n_cases = 34
    
    # Outcomes: 11 Fatal, 23 Recovered
    outcomes = ['Fatal'] * 11 + ['Recovered'] * 23
    np.random.shuffle(outcomes)
    
    # Initialize list
    cases = []
    
    # Index case (Case 1)
    index_onset = datetime(2018, 11, 2) # Approximate start
    cases.append({
        'case_id': 1,
        'date_of_onset': index_onset.strftime('%Y-%m-%d'),
        'outcome': outcomes[0],
        'infector_id': 'Zoonotic',
        'generation': 1
    })
    
    # Generate subsequent cases
    current_generation_cases = [1]
    next_case_id = 2
    generation = 2
    
    # Simulating R0 ~ 2.1 using a Poisson distribution for secondary cases
    while next_case_id <= n_cases and current_generation_cases:
        next_gen_cases = []
        for infector in current_generation_cases:
            if next_case_id > n_cases:
                break
                
            # Number of secondary cases for this infector
            # To ensure we hit exactly 34, we adjust probabilities or just draw until n_cases is reached
            n_secondary = np.random.poisson(2.1)
            
            # Cap secondary cases if we exceed 34
            if next_case_id + n_secondary - 1 > n_cases:
                n_secondary = n_cases - next_case_id + 1
                
            for _ in range(n_secondary):
                # Incubation period: lognormal or uniform between 9-40
                incubation_days = int(np.random.uniform(9, 40))
                
                # Find infector's onset date
                infector_onset = datetime.strptime([c['date_of_onset'] for c in cases if c['case_id'] == infector][0], '%Y-%m-%d')
                
                # Assuming transmission happens around onset +/- a few days
                transmission_delay = int(np.random.normal(0, 3))
                transmission_date = infector_onset + timedelta(days=transmission_delay)
                onset_date = transmission_date + timedelta(days=incubation_days)
                
                cases.append({
                    'case_id': next_case_id,
                    'date_of_onset': onset_date.strftime('%Y-%m-%d'),
                    'outcome': outcomes[next_case_id - 1],
                    'infector_id': infector,
                    'generation': generation
                })
                next_gen_cases.append(next_case_id)
                next_case_id += 1
                
        current_generation_cases = next_gen_cases
        generation += 1

    # If we didn't reach 34 (branching process died out early), force assign remaining to recent generations
    while next_case_id <= n_cases:
        infector = np.random.choice([c['case_id'] for c in cases if c['case_id'] != next_case_id])
        incubation_days = int(np.random.uniform(9, 40))
        infector_onset = datetime.strptime([c['date_of_onset'] for c in cases if c['case_id'] == infector][0], '%Y-%m-%d')
        onset_date = infector_onset + timedelta(days=incubation_days)
        cases.append({
            'case_id': next_case_id,
            'date_of_onset': onset_date.strftime('%Y-%m-%d'),
            'outcome': outcomes[next_case_id - 1],
            'infector_id': infector,
            'generation': max([c['generation'] for c in cases]) + 1
        })
        next_case_id += 1
        
    df = pd.DataFrame(cases)
    df = df.sort_values('date_of_onset')
    df.to_csv('/Users/jasonandrews/repos/hanta/data/epuyen_2018_cases.csv', index=False)
    print("Generated data/epuyen_2018_cases.csv")

if __name__ == "__main__":
    generate_epuyen_data()
