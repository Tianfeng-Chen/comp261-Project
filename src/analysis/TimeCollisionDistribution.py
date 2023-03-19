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

# Extract collision times and dates
collision_times = []
for item in data:
    time_str = item['crash_time']
    hour = int(time_str.split(':')[0])
    collision_times.append(hour)

# Plot histogram of collisions per hour
plt.hist(collision_times, bins=24, edgecolor='black', alpha=0.5)
plt.xticks(range(24))
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Collisions')
plt.title('Distribution of Collisions by Time of Day')
plt.show()
