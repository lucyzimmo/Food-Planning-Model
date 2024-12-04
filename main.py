"""
This script demonstrates how to use linear programming to optimize the allocation of supermarkets 
in Imperial County, California.
"""
import pandas as pd
from pulp import LpProblem, LpVariable, LpInteger, LpMaximize, lpSum, PULP_CBC_CMD, LpBinary
import numpy as np
import json
<<<<<<< Updated upstream
=======
import geopandas as gpd
import matplotlib.pyplot as plt
>>>>>>> Stashed changes

# Load the provided data
file_path = 'data/food_access_research_atlas.csv'
food_data = pd.read_csv(file_path)

adjacency_file_path = 'adjacency.json'
with open(adjacency_file_path, 'r') as f:
    adjacency = json.load(f)

# Filter data for Imperial County, California
imperial_county_data = food_data[(food_data['County'] == 'Imperial') & (food_data['State'] == 'California')]

# Select relevant columns for supermarket allocation baseline
selected_columns = ['CensusTract', 'POP2010', 'TractSNAP', 'MedianFamilyIncome']
imperial_county_data = imperial_county_data[selected_columns]

# Define constants
TOTAL_NEW_SUPERMARKETS = 30
ADJACENCY_LIMIT = 6
MEDIAN_INCOME_THRESHOLD = 30000 # median income for poverty threshold
MAX_SUPERMARKETS_PER_TRACT = 1
ALPHA = 0.7 # weight for low-income household coverage
BETA = 0.3  # weight for population coverage

# Prepare data for optimization
tracts = imperial_county_data['CensusTract'].tolist()
population = dict(zip(tracts, imperial_county_data['POP2010']))
low_income_households = dict(zip(tracts, imperial_county_data['TractSNAP']))
median_income = dict(zip(tracts, imperial_county_data['MedianFamilyIncome']))

# Adjust adjacency keys
adjacency = {
    tract[1:]: [neighbor[1:] for neighbor in neighbors]
    for tract, neighbors in adjacency.items()
}

# Normalize keys
tracts = [str(tract) for tract in tracts]
low_income_households = {str(k): v for k, v in low_income_households.items()}
population = {str(k): v for k, v in population.items()}
median_income = {str(k): v for k, v in median_income.items()}

# Define the problem
problem = LpProblem("SupermarketAllocation", LpMaximize)

# Define decision variables
supermarkets = {
    tract: LpVariable(f"supermarkets_{tract}", 0, MAX_SUPERMARKETS_PER_TRACT, LpInteger)
    for tract in tracts
}

# Add binary variables to indicate if a tract has any supermarkets
has_supermarket = {
    tract: LpVariable(f"has_supermarket_{tract}", 0, 1, LpBinary)
    for tract in tracts
}

# Link `supermarkets` and `has_supermarket` variables
for tract in tracts:
    problem += supermarkets[tract] - MAX_SUPERMARKETS_PER_TRACT * has_supermarket[tract] <= 0, f"LinkBinary_{tract}"

# Normalize metrics
max_population = max(population.values())
max_low_income = max(low_income_households.values())

# Objective function
mean_income = np.mean(list(median_income.values()))
problem += (
    lpSum([
        ALPHA * (low_income_households[tract] / max_low_income) * supermarkets[tract] +
        BETA * (population[tract] / max_population) * supermarkets[tract]
        for tract in tracts
    ])
    - lpSum([
        has_supermarket[tract] * (median_income[tract] - mean_income) ** 2
        for tract in tracts
    ])
), "MaximizeCombinedCoverageAndMinimizeVariance"

# Total supermarkets allocation
problem += lpSum(supermarkets.values()) == TOTAL_NEW_SUPERMARKETS, "TotalSupermarketsLimit"

# Adjacency limit
filtered_adjacency = {
    tract: [neighbor for neighbor in neighbors if neighbor in supermarkets]
    for tract, neighbors in adjacency.items()
    if tract in supermarkets
}

seen = set()
for tract, neighbors in filtered_adjacency.items():
    for neighbor in neighbors:
        if (tract, neighbor) not in seen and (neighbor, tract) not in seen:
            problem += supermarkets[tract] + supermarkets[neighbor] <= ADJACENCY_LIMIT, f"AdjacencyLimit_{tract + " " + neighbor}"
            seen.add((tract, neighbor))
            seen.add((neighbor, tract))

# Solve the problem
solver = PULP_CBC_CMD(msg=True)
problem.solve(solver)

# Assign results
imperial_county_data['CensusTract'] = imperial_county_data['CensusTract'].astype(str)
imperial_county_data['Assigned_Supermarkets'] = imperial_county_data['CensusTract'].map(
    lambda tract: supermarkets[tract].varValue
)

# Save results
output_file_path = 'assigned_supermarkets.csv'
imperial_county_data.to_csv(output_file_path, index=False)
print(f"Supermarket allocation results saved to: {output_file_path}")

# Output results
print("Optimization Status:", problem.status)
for tract in tracts:
    print(f"Census Tract {tract}: {supermarkets[tract].varValue} supermarkets")

debuggingFile = 'debugLP.lp'
problem.writeLP(debuggingFile)

# visualization
"imperial_county.xlsx"
imperial = gpd.read_file("imperial_county_supp/imperial_county.shp")
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
imperial.plot(column="TractSNAP", ax=ax, edgecolor="floralwhite", vmin=0, vmax=1000, linewidth=0.5, legend=True, legend_kwds={'label': "Tract Snap", 'orientation': "vertical"})
plt.title("Imperial County Population Receiving Snap by Tracts, 2010")
plt.savefig('tract_snap.svg', bbox_inches='tight')

fig2 = plt.figure()
ax2 = fig2.add_axes([0, 0, 1, 1])
imperial.plot(column="POP2010", ax=ax2, edgecolor="floralwhite", vmin=100, vmax=13000, linewidth=0.5, legend=True, legend_kwds={'label': "Population 2010", 'orientation': "vertical"})
plt.title("Imperial County Population 2010 by Tracts")
plt.savefig('population.svg', bbox_inches='tight')

fig3 = plt.figure()
ax3 = fig3.add_axes([0, 0, 1, 1])
imperial.plot(column="PovertyRat", ax=ax3, edgecolor="floralwhite", vmin=0, vmax=100, linewidth=0.5, legend=True, legend_kwds={'label': "PovertyRate", 'orientation': "vertical"})
plt.title("Imperial County Poverty Rate Tract, 2010")
plt.savefig('povertyrate.svg', bbox_inches='tight')

fig4 = plt.figure()
ax4 = fig4.add_axes([0, 0, 1, 1])
imperial.plot(column="GEOID10", ax=ax4, edgecolor="floralwhite", legend=True)
plt.title("Imperial County Tract IDs")
plt.savefig('tractmap.svg', bbox_inches='tight')