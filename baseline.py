"""
This script generates a random allocation of supermarkets to census tracts in Imperial County, California, 
and is our baseline for comparison with other optimization methods."""
import pandas as pd
import numpy as np

np.random.seed(0)  # set constant seed for reproducibility

# Load the provided data
file_path = 'data/food_access_research_atlas.csv'
food_data = pd.read_csv(file_path)

# Filter data for Imperial County, California
imperial_county_data = food_data[(food_data['County'] == 'Imperial') & (food_data['State'] == 'California')]



# Select relevant columns for supermarket allocation baseline
selected_columns = ['CensusTract', 'POP2010', 'TractSNAP']
imperial_county_data = imperial_county_data[selected_columns]

# Define the total number of supermarkets to be distributed
TOTAL_NEW_SUPERMARKETS = 100

# Step 1: Create Random Allocation of Supermarkets
# Generate random allocations that sum to TOTAL_NEW_SUPERMARKETS
random_weights = np.random.dirichlet(np.ones(len(imperial_county_data)), size=1)
imperial_county_data['Random_Allocation'] = (random_weights[0] * TOTAL_NEW_SUPERMARKETS).round()

# Step 2: Adjust to Match TOTAL_NEW_SUPERMARKETS exactly
initial_total = imperial_county_data['Random_Allocation'].sum()
difference = TOTAL_NEW_SUPERMARKETS - int(initial_total)

if difference > 0:
    # Add supermarkets randomly to make up the difference
    add_indices = np.random.choice(imperial_county_data.index, size=difference, replace=False)
    imperial_county_data.loc[add_indices, 'Random_Allocation'] += 1
elif difference < 0:
    # Remove supermarkets randomly to match the total
    remove_indices = np.random.choice(imperial_county_data.index, size=abs(difference), replace=False)
    imperial_county_data.loc[remove_indices, 'Random_Allocation'] -= 1

# Renaming column for clarity
imperial_county_data = imperial_county_data.rename(columns={'Random_Allocation': 'Assigned_Supermarkets'})

# Save as output file
output_file_path = 'assigned_supermarkets_random.csv'
imperial_county_data.to_csv(output_file_path, index=False)
print(f"Random supermarket allocation results saved to: {output_file_path}")
