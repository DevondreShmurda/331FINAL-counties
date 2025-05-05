import pandas as pd
import numpy as np
import os

# --- Load files from Downloads folder ---
farm_2017 = pd.read_csv('/Users/devononeill/Downloads/DB46C06C-B214-3982-903A-CBA6DB21B303.csv')
farm_2022 = pd.read_csv('/Users/devononeill/Downloads/B37EA3BC-08B7-3338-A326-E7A7B38DDB87.csv')

agri_2017 = pd.read_csv('/Users/devononeill/Downloads/F3EC6C76-8D95-307E-A1C5-6E305CF7197D.csv')
agri_2017['Value'] = agri_2017['Value'].str.replace(',', '', regex=True)
agri_2017['Value'] = pd.to_numeric(agri_2017['Value'], errors='coerce')

agri_2022 = pd.read_csv('/Users/devononeill/Downloads/82B7478E-16BA-3142-9D60-CBFFE0007410.csv')
agri_2022['Value'] = agri_2022['Value'].str.replace(',', '', regex=True)
agri_2022['Value'] = pd.to_numeric(agri_2022['Value'], errors='coerce')

# --- Define Montana counties ---
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

# --- Define extraction function ---
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

# --- Rename County to lowercase 'county' ---
farm_2017_data = farm_2017_data.rename(columns={'County': 'county'})
farm_2022_data = farm_2022_data.rename(columns={'County': 'county'})
agri_2017_data = agri_2017_data.rename(columns={'County': 'county'})
agri_2022_data = agri_2022_data.rename(columns={'County': 'county'})

# --- Merge all datasets ---
master = farm_2017_data.merge(farm_2022_data, on='county', how='outer')
master = master.merge(agri_2017_data, on='county', how='left')
master = master.merge(agri_2022_data, on='county', how='left')

# --- Add State Column ---
master['state'] = 'Montana'

# --- Convert numeric values first ---
for col in ['farms_2017', 'farms_2022', 'agri_2017', 'agri_2022']:
    master[col] = pd.to_numeric(master[col], errors='coerce')

# --- Calculate Changes ---
master['farm_net_change'] = master['farms_2022'] - master['farms_2017']
master['farm_pct_change'] = ((master['farms_2022'] - master['farms_2017']) / master['farms_2017']) * 100
master['agri_net_change'] = master['agri_2022'] - master['agri_2017']
master['agri_pct_change'] = ((master['agri_2022'] - master['agri_2017']) / master['agri_2017']) * 100

# --- Handle rounding and formatting changes ---
for col in ['farm_net_change', 'agri_net_change']:
    master[col] = master[col].round(0).astype('Int64')

for col in ['farm_pct_change', 'agri_pct_change']:
    master[col] = master[col].round(2)

# --- Handle displaying (D) where missing ---
def format_value(x):
    if pd.isna(x):
        return '(D)'
    else:
        return "{:,.0f}".format(x)

master['farms_2017'] = master['farms_2017'].apply(format_value)
master['farms_2022'] = master['farms_2022'].apply(format_value)
master['agri_2017'] = master['agri_2017'].apply(format_value)
master['agri_2022'] = master['agri_2022'].apply(format_value)

# --- Reorder Columns ---
master = master[['state', 'county', 
                 'farms_2017', 'farms_2022', 
                 'agri_2017', 'agri_2022', 
                 'farm_net_change', 'farm_pct_change', 
                 'agri_net_change', 'agri_pct_change']]

# --- Save the Clean Montana Output ---
output_path = '/Users/devononeill/Downloads/Montana_Farm_Agri_Clean.csv'
master.to_csv(output_path, index=False)

print(f"✅ Montana clean file created: {output_path}")
print(master.head())
