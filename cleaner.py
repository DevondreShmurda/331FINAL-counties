import pandas as pd
import os

# --- Path to your Montana cleaned file ---
montana_clean_path = '/Users/devononeill/Downloads/Montana_Farm_Agri_Clean.csv'

# --- Path to the new Big Master File ---
america_master_path = '/Users/devononeill/Downloads/America_Farm_Agri_Clean.csv'

# --- Load Montana clean file ---
montana_data = pd.read_csv(montana_clean_path)

# --- Check if America Master already exists ---
if os.path.exists(america_master_path):
    america_master = pd.read_csv(america_master_path)
    america_master = pd.concat([america_master, montana_data], ignore_index=True)
else:
    america_master = montana_data

# --- Save updated America Master ---
america_master.to_csv(america_master_path, index=False)

print(f"✅ Montana data successfully added to America Master File: {america_master_path}")
print(america_master.tail())
