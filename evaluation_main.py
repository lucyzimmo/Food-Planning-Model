"""
This script calculates the evaluation metrics for the assigned supermarkets."""
import pandas as pd
import numpy as np

# Load the provided data file
file_path = 'assigned_supermarkets.csv'
file_path_proportional = 'assigned_supermarket_proportional.csv'
file_path_baseline = 'assigned_supermarkets_random.csv'
main = pd.read_csv(file_path)
proportional = pd.read_csv(file_path_proportional)
baseline = pd.read_csv(file_path_baseline)

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

# Metric 3: Combined Coverage (Population & Low-Income Households & Geographic)
def combined_coverage(data, alpha=0.4, beta=0.4, gamma=0.2):
    low_income_coverage = coverage_of_low_income_households(data)
    population_coverage_value = population_coverage(data)
    geographic_coverage_value = geographic_coverage(data)
    combined = alpha * low_income_coverage + beta * population_coverage_value + gamma * geographic_coverage_value
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

# Metric 5: Geographic Coverage
def geographic_coverage(data):
    # Count the number of tracts with at least one supermarket
    tracts_with_supermarkets = data[data['Assigned_Supermarkets'] > 0].shape[0]
    total_tracts = data.shape[0]
    return (tracts_with_supermarkets / total_tracts) * 100 if total_tracts > 0 else 0

# Calculate and print each metric
low_income_coverage = coverage_of_low_income_households(main)
low_income_coverage_p = coverage_of_low_income_households(proportional)
low_income_coverage_b = coverage_of_low_income_households(baseline)
population_coverage_value = population_coverage(main)
population_coverage_value_p = population_coverage(proportional)
population_coverage_value_b = population_coverage(baseline)
geographic_coverage_value = geographic_coverage(main)
geographic_coverage_value_p = geographic_coverage(proportional)
geographic_coverage_value_b = geographic_coverage(baseline)
combined_coverage_value = combined_coverage(main, alpha=0.4, beta=0.4, gamma=0.2)
combined_coverage_value_p = combined_coverage(proportional, alpha=0.4, beta=0.4, gamma=0.2)
combined_coverage_value_b = combined_coverage(baseline, alpha=0.4, beta=0.4, gamma=0.2)
income_balance_variance = household_income_balance(main)
income_balance_variance_p = household_income_balance(proportional)

# Display results
print(f"Coverage of Low-Income Households: main: {low_income_coverage:.2f}% proportional: {low_income_coverage_p:.2f}% baseline: {low_income_coverage_b:.2f}%")
print(f"Population Coverage: main: {population_coverage_value:.2f}% proportional: {population_coverage_value_p:.2f}%  baseline: {population_coverage_value_b:.2f}%")
print(f"Geographic Coverage: main: {geographic_coverage_value:.2f}% proportional: {geographic_coverage_value_p:.2f}%  baseline: {geographic_coverage_value_b:.2f}%")
print(f"Combined Coverage: main: {combined_coverage_value:.2f}% proportional: {combined_coverage_value_p:.2f}% baseline: {combined_coverage_value_b:.2f}%")
print(f"Household Income Balance: main: {income_balance_variance:.2f} proportional: {income_balance_variance_p:.2f} baseline: not applicable")
