import json
import matplotlib.pyplot as plt

# Load collision data from local JSON file
data = []
with open('collision_data.json', 'r') as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError:
            continue

# Validate the data
valid_data = []
for item in data:
    if 'contributing_factor_vehicle_1' in item and 'contributing_factor_vehicle_2' in item:
        valid_data.append(item)

# Extract the number of collisions for each factor for both vehicles
factor_counts = {}
for item in valid_data:
    factor1 = item['contributing_factor_vehicle_1']
    factor2 = item['contributing_factor_vehicle_2']
    if factor1 != "Unspecified":
        if factor1 not in factor_counts:
            factor_counts[factor1] = 0
        factor_counts[factor1] += 1

    if factor2 != "Unspecified":
        if factor2 not in factor_counts:
            factor_counts[factor2] = 0
        factor_counts[factor2] += 1

# Sort the factors by collision count
sorted_counts = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)

# Extract the top 20 factors and their counts
top_counts = dict(sorted_counts[:20])

# Increase figure size and plot a bar chart of the top 20 factors that caused the collision for both vehicles
plt.figure(figsize=(10, 6))
plt.bar(top_counts.keys(), top_counts.values(), color='blue')
plt.xticks(rotation=90)
plt.xlabel('Contributing Factor')
plt.ylabel('Number of Collisions')
plt.title('Top 20 Factors Contributing to Collisions for Both Vehicles')

# Show the plot
plt.show()
