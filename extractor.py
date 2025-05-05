import pandas as pd
import numpy as np
import os

# --- CHANGE THESE INPUTS ---
state_name = 'Montana'  # <<< UPDATE: Example: 'Montana', 'Texas', 'Wyoming'

farm_2017_path = '/Users/devononeill/Downloads/DB46C06C-B214-3982-903A-CBA6DB21B303.csv'  # <<< UPDATE PATH
farm_2022_path = '/Users/devononeill/Downloads/B37EA3BC-08B7-3338-A326-E7A7B38DDB87.csv'  # <<< UPDATE PATH
agri_2017_path = '/Users/devononeill/Downloads/F3EC6C76-8D95-307E-A1C5-6E305CF7197D.csv'  # <<< UPDATE PATH
agri_2022_path = '/Users/devononeill/Downloads/82B7478E-16BA-3142-9D60-CBFFE0007410.csv'  # <<< UPDATE PATH

# Example: UPDATE county names for your state
counties = [
    'Beaverhead', 'Big Horn', 'Blaine', 'Broadwater', 'Carbon', 'Carter', 'Cascade', 'Chouteau', 'Custer',
    'Daniels', 'Dawson', 'Deer Lodge', 'Fallon', 'Fergus', 'Flathead', 'Gallatin', 'Garfield', 'Glacier',
    'Golden Valley', 'Granite', 'Hill', 'Jefferson', 'Judith Basin', 'Lake', 'Lewis and Clark', 'Liberty',
    'Lincoln', 'McCone', 'Madison', 'Meagher', 'Mineral', 'Missoula', 'Musselshell', 'Park', 'Petroleum',
    'Phillips', 'Pondera', 'Powder River', 'Powell', 'Prairie', 'Ravalli', 'Richland', 'Roosevelt', 'Rosebud',
    'Sanders', 'Sheridan', 'Silver Bow', 'Stillwater', 'Sweet Grass', 'Teton', 'Toole', 'Treasure', 'Valley',
    'Wheatland', 'Wibaux', 'Yellowstone'
]
counties_upper = [c.upper() for c in counties]

# --- Load data ---
farm_2017 = pd.read_csv(farm_2017_path)
farm_2022 = pd.read_csv(farm_2022_path)

agri_2017 = pd.read_csv(agri_2017_path)
agri_2017['Value'] = agri_2017['Value'].str.replace(',', '', regex=True)
agri_2017['Value'] = pd.to_numeric(agri_2017['Value'], errors='coerce')

agri_2022 = pd.read_csv(agri_2022_path)
agri_2022['Value'] = agri_2022['Value'].str.replace(',', '', regex=True)
agri_2022['Value'] = pd.to_numeric(agri_2022['Value'], errors='coerce')

# --- Extraction function ---
def extract_values(df, counties, year_label):
    df.columns = df.columns.str.strip().str.title()
    df['County'] = df['County'].str.strip().str.upper()
    result = df[df['County'].isin(counties)].copy()
    result = result[['County', 'Value']]
    result = result.rename(columns={'Value': year_label})
    return result

# --- Extract values ---
farm_2017_data = extract_values(farm_2017, counties_upper, 'farms_2017')
farm_2022_data = extract_values(farm_2022, counties_upper, 'farms_2022')
agri_2017_data = extract_values(agri_2017, counties_upper, 'agri_2017')
agri_2022_data = extract_values(agri_2022, counties_upper, 'agri_2022')

# --- Merge datasets ---
for df in [farm_2017_data, farm_2022_data, agri_2017_data, agri_2022_data]:
    df.rename(columns={'County': 'county'}, inplace=True)

master = farm_2017_data.merge(farm_2022_data, on='county', how='outer')
master = master.merge(agri_2017_data, on='county', how='left')
master = master.merge(agri_2022_data, on='county', how='left')

# --- Add State Column ---
master['state'] = state_name

# --- Convert to numeric BEFORE math ---
for col in ['farms_2017', 'farms_2022', 'agri_2017', 'agri_2022']:
    master[col] = pd.to_numeric(master[col], errors='coerce')

# --- Calculate Changes ---
master['farm_net_change'] = master['farms_2022'] - master['farms_2017']
master['farm_pct_change'] = ((master['farms_2022'] - master['farms_2017']) / master['farms_2017']) * 100
master['agri_net_change'] = master['agri_2022'] - master['agri_2017']
master['agri_pct_change'] = ((master['agri_2022'] - master['agri_2017']) / master['agri_2017']) * 100

# --- Round properly ---
for col in ['farm_net_change', 'agri_net_change']:
    master[col] = master[col].round(0).astype('Int64')

for col in ['farm_pct_change', 'agri_pct_change']:
    master[col] = master[col].round(2)

# --- Format missing numbers as (D) and format numbers nicely ---
def format_value(x):
    if pd.isna(x):
        return '(D)'
    else:
        return "{:,.0f}".format(x)

master['farms_2017'] = master['farms_2017'].apply(format_value)
master['farms_2022'] = master['farms_2022'].apply(format_value)
master['agri_2017'] = master['agri_2017'].apply(format_value)
master['agri_2022'] = master['agri_2022'].apply(format_value)

# --- Final column order ---
master = master[['state', 'county',
                 'farms_2017', 'farms_2022',
                 'agri_2017', 'agri_2022',
                 'farm_net_change', 'farm_pct_change',
                 'agri_net_change', 'agri_pct_change']]

# --- Save Output ---
output_path = f'/Users/devononeill/Downloads/{state_name}_Farm_Agri_Clean.csv'
master.to_csv(output_path, index=False)

print(f"✅ {state_name} clean file created: {output_path}")
print(master.head())
