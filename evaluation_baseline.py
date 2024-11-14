import pandas as pd

# Load the assigned supermarket data
file_path = 'assigned_supermarkets_random.csv'
imperial_county_data = pd.read_csv(file_path)

# Calculate Geographic Coverage
def calculate_geographic_coverage(data):
    # Count the number of tracts with at least one supermarket
    tracts_with_supermarkets = data[data['Assigned_Supermarkets'] > 0].shape[0]
    total_tracts = data.shape[0]
    geographic_coverage = (tracts_with_supermarkets / total_tracts) * 100  # percentage
    return geographic_coverage

# Calculate Population Coverage
def calculate_population_coverage(data):
    # Sum the population in tracts with at least one supermarket
    population_served = data[data['Assigned_Supermarkets'] > 0]['POP2010'].sum()
    total_population = data['POP2010'].sum()
    population_coverage = (population_served / total_population) * 100  # percentage
    return population_coverage

# Run the evaluation
geographic_coverage = calculate_geographic_coverage(imperial_county_data)
population_coverage = calculate_population_coverage(imperial_county_data)

# Print the evaluation results
print(f"Geographic Coverage: {geographic_coverage:.2f}% of tracts have at least one supermarket.")
print(f"Population Coverage: {population_coverage:.2f}% of the population is served by tracts with supermarkets.")
