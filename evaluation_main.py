import pandas as pd
import numpy as np

# Load the provided data file
file_path = 'assigned_supermarkets.csv'
imperial_county_data = pd.read_csv(file_path)

# Metric 1: Coverage of Low-Income Households
def coverage_of_low_income_households(data):
    total_low_income_households = data['TractSNAP'].sum()
    served_low_income_households = data[data['Assigned_Supermarkets'] > 0]['TractSNAP'].sum()
    coverage = (served_low_income_households / total_low_income_households) * 100
    return coverage

# Metric 2: Population Coverage
def population_coverage(data):
    total_population = data['POP2010'].sum()
    served_population = data[data['Assigned_Supermarkets'] > 0]['POP2010'].sum()
    coverage = (served_population / total_population) * 100
    return coverage

# Metric 3: Combined Coverage (Population & Low-Income Households)
def combined_coverage(data, alpha=0.5, beta=0.5):
    low_income_coverage = coverage_of_low_income_households(data)
    population_coverage_value = population_coverage(data)
    combined = alpha * low_income_coverage + beta * population_coverage_value
    return combined

# Metric 4: Household Income Balance (Using Median Family Income)
def household_income_balance(data):
    # Filter tracts with at least one assigned supermarket
    tracts_with_food_banks = data[data['Assigned_Supermarkets'] > 0]
    if not tracts_with_food_banks.empty:
        # Calculate variance of MedianFamilyIncome
        average_income = tracts_with_food_banks['MedianFamilyIncome'].mean()
        variance_income = ((tracts_with_food_banks['MedianFamilyIncome'] - average_income) ** 2).mean()
    else:
        variance_income = np.nan  # No food banks assigned case
    return variance_income

# Calculate and print each metric
low_income_coverage = coverage_of_low_income_households(imperial_county_data)
population_coverage_value = population_coverage(imperial_county_data)
combined_coverage_value = combined_coverage(imperial_county_data, alpha=0.5, beta=0.5)
income_balance_variance = household_income_balance(imperial_county_data)

# Display results
print(f"Coverage of Low-Income Households: {low_income_coverage:.2f}%")
print(f"Population Coverage: {population_coverage_value:.2f}%")
print(f"Combined Coverage: {combined_coverage_value:.2f}%")
print(f"Household Income Balance: {income_balance_variance:.2f}")
