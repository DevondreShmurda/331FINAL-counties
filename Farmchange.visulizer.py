import pandas as pd
import matplotlib.pyplot as plt

# --- Load the America Master File ---
america_master_path = '/Users/devononeill/Downloads/America_Farm_Agri_Clean.csv'
data = pd.read_csv(america_master_path)

# --- Filter for Montana counties only (if needed) ---
montana_data = data[data['state'] == 'Montana']

# --- Only keep counties with numeric farm % change ---
montana_data = montana_data[pd.to_numeric(montana_data['farm_pct_change'], errors='coerce').notna()]

# --- Plot ---
plt.figure(figsize=(16,8))
plt.bar(montana_data['county'], montana_data['farm_pct_change'], color='skyblue')
plt.xticks(rotation=90, fontsize=8)
plt.title('Montana Counties: % Change in Number of Farms (2017–2022)', fontsize=16)
plt.ylabel('% Change', fontsize=14)
plt.xlabel('County', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# --- Save chart ---
plt.savefig('/Users/devononeill/Downloads/Montana_Farm_Percent_Change.png')
print("✅ Bar chart saved as Montana_Farm_Percent_Change.png!")
plt.show()
