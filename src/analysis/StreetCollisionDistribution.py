import json
import matplotlib.pyplot as plt

# Load collision data from local JSON file
data = []
with open('collision_data.json', 'r') as f:
    for line in f:
        try:
            item = json.loads(line)
            if 'on_street_name' in item:
                data.append(item)
        except json.JSONDecodeError:
            continue
            
# Extract street names and counts
street_counts = {}
for item in data:
    street_name = item['on_street_name']
    if street_name not in street_counts:
        street_counts[street_name] = 0
    street_counts[street_name] += 1

# Sort street counts in descending order
sorted_street_counts = dict(sorted(street_counts.items(), key=lambda item: item[1], reverse=True)[:50])

# Plot bar chart
plt.figure(figsize=(20, 15))
plt.bar(sorted_street_counts.keys(), sorted_street_counts.values())
plt.xticks(rotation=90)
plt.xlabel('Street Name')
plt.ylabel('Number of Collisions')
plt.title('Top 50 Streets with the Most Collisions')
plt.ylim(top=max(sorted_street_counts.values()) + 1000)
plt.show()


