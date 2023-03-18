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

# Extract collision hour and count
collision_hours = {}
for item in data:
    try:
        collision_time = item['collision_time']
        collision_hour = int(collision_time.split(':')[0])
        if collision_hour not in collision_hours:
            collision_hours[collision_hour] = 0
        collision_hours[collision_hour] += 1
    except KeyError:
        continue

# Plot distribution of collision numbers by hour
plt.figure(figsize=(10, 6))
plt.bar(collision_hours.keys(), collision_hours.values())
plt.xlabel('Hour')
plt.ylabel('Number of Collisions')
plt.title('Distribution of Collisions by Hour')
plt.show()
