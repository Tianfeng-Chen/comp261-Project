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
    if 'vehicle_type_code1' in item and 'vehicle_type_code2' in item:
        valid_data.append(item)

# Group the vehicle types into categories
vehicle_categories = {
    'sedan': ['sedan', 'convertible', 'hatchback', 'wagon', '4 dr sedan', '4 dr sedan/hardtop', '4 dr wagon', 'utility', 'camper', 'van camper', 'limousine'],
    'SUV': ['suv', 'jeep', 'pick-up truck', 'sport utility / station wagon', 'sport utility vehicle'],
    'truck': ['dump', 'tanker', 'tractor truck diesel', 'tractor truck gasoline', 'tractor truck diesel', 'tow truck / wrecker', 'box truck', 'flat bed', 'garbage or refuse'],
    'motorcycle': ['motorcycle', 'scooter', 'motorbike', 'dirt bike'],
    'bike': ['bicycle', 'e-bike'],
    'public transport': ['taxi', 'bus', 'ambulance', 'van']
}

# Initialize the vehicle counts for each category to 0
vehicle_counts = {category: 0 for category in vehicle_categories}

# Count the number of collisions for each vehicle
for item in valid_data:
    vehicle1 = item['vehicle_type_code1']
    vehicle2 = item['vehicle_type_code2']

    for category, types in vehicle_categories.items():
        if vehicle1.lower() in types or vehicle2.lower() in types:
            vehicle_counts[category] += 1
            break

# Plot a pie chart of the vehicle types by category
plt.pie(vehicle_counts.values(), labels=vehicle_counts.keys(), autopct='%1.1f%%')
plt.title('Vehicle Types Involved in Collisions by Category')
plt.show()

# Plot a bar chart of the vehicle types by category
plt.bar(vehicle_counts.keys(), vehicle_counts.values(), color='blue')
plt.xticks(rotation=90)
plt.xlabel('Vehicle Category')
plt.ylabel('Number of Collisions')
plt.title('Vehicle Types Involved in Collisions by Category')
plt.show()

