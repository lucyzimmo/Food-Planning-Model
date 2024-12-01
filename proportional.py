"""This script calculates the initial supermarket allocation based on population proportion 
for Imperial County, California."""
import pandas as pd

# Load the provided data
file_path = 'data/food_access_research_atlas.csv'
food_data = pd.read_csv(file_path)

# Filter data for Imperial County, California
imperial_county_data = food_data[(food_data['County'] == 'Imperial') & (food_data['State'] == 'California')]

# Select relevant columns for supermarket allocation baseline
# Population (POP2010) and SNAP usage (TractSNAP) for additional analysis if needed
selected_columns = ['CensusTract', 'POP2010', 'TractSNAP', 'MedianFamilyIncome']
imperial_county_data = imperial_county_data[selected_columns]

# Define the total number of supermarkets to be distributed
TOTAL_NEW_SUPERMARKETS = 100  # to act as a percentage

# Step 1: Calculate Population Proportion
total_population = imperial_county_data['POP2010'].sum()
imperial_county_data['Population_Proportion'] = imperial_county_data['POP2010'] / total_population

# Step 2: Initial Supermarket Allocation Based on Population Proportion
imperial_county_data['Initial_Supermarkets'] = (imperial_county_data['Population_Proportion'] * TOTAL_NEW_SUPERMARKETS).round()

# Step 3: Adjust to Match TOTAL_NEW_SUPERMARKETS exactly
initial_total = imperial_county_data['Initial_Supermarkets'].sum()

# Calculate difference to adjust to TOTAL_NEW_SUPERMARKETS
difference = TOTAL_NEW_SUPERMARKETS - int(initial_total)

# Adjustment based on population proportion
if difference > 0:
    # Add supermarkets to tracts with the highest population proportion
    imperial_county_data = imperial_county_data.sort_values('Population_Proportion', ascending=False)
    imperial_county_data.iloc[:difference, imperial_county_data.columns.get_loc('Initial_Supermarkets')] += 1
elif difference < 0:
    # Remove supermarkets from tracts with the lowest population proportion
    imperial_county_data = imperial_county_data.sort_values('Population_Proportion')
    imperial_county_data.iloc[:abs(difference), imperial_county_data.columns.get_loc('Initial_Supermarkets')] -= 1

# Renaming column for clarity
imperial_county_data = imperial_county_data.rename(columns={'Initial_Supermarkets': 'Assigned_Supermarkets'})

# Save as output file
output_file_path = 'assigned_supermarket_proportional.csv'
imperial_county_data.to_csv(output_file_path, index=False)
print(f"Supermarket allocation results saved to: {output_file_path}")


