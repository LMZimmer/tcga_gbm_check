import pandas as pd
from datetime import timedelta
import json
import sys

excel_path = 'TCIA_TCGA-GBM_09-16-2015-nbia-digest.xlsx'
a_output = 'patient_series_dates.json'
min_time_diff_weeks = 12

# Load
df = pd.read_excel(excel_path)
df['Series Date'] = pd.to_datetime(df['Series Date'], errors='coerce')

# Created Patient_id : List[dates] dictionary
patient_dates = {}
for pid, group in df.groupby('Patient ID'):
    dates = sorted(set(group['Series Date'].dropna()))
    patient_dates[pid] = [d.date().isoformat() for d in dates]

# Save
with open(a_output, 'w') as f:
    json.dump(patient_dates, f, indent=2)

# Identify patients with exams 12 weeks apart
threshold_weeks = timedelta(weeks=min_time_diff_weeks)
count = 0
for pid, dates in patient_dates.items():
    if not dates:
        continue
    earliest = pd.to_datetime(dates[0])
    if any(pd.to_datetime(d) >= earliest + threshold_weeks for d in dates):
        count += 1

print(f'Dictionary saved to: {a_output}')
print(f'Number of patients with a date >= 12 weeks after earliest: {count}')
