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
    if 'vehicle_type_code1' in item and 'vehicle_type_code2' in item and 'number_of_persons_injured' in item:
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

# Initialize the injury counts for each category to 0
injury_counts = {category: 0 for category in vehicle_categories}

# Count the number of collisions and injuries for each vehicle
for item in valid_data:
    vehicle1 = item['vehicle_type_code1'].lower()
    vehicle2 = item['vehicle_type_code2'].lower()
    injuries = int(item['number_of_persons_injured'])

    # Check if either vehicle is in one of the vehicle categories
    category1 = None
    category2 = None
    for category, types in vehicle_categories.items():
        if vehicle1 in types:
            category1 = category
        if vehicle2 in types:
            category2 = category

    # Increment the counts for each vehicle category and injury category
    if category1 is not None:
        vehicle_counts[category1] += 1
        injury_counts[category1] += injuries
    if category2 is not None:
        vehicle_counts[category2] += 1
        injury_counts[category2] += injuries

# Plot a bar chart of the vehicle types by number of injuries
plt.bar(injury_counts.keys(), injury_counts.values(), color='blue')
plt.xticks(rotation=90)
plt.xlabel('Vehicle Type')
plt.ylabel('Number of Injuries')
plt.title('Vehicle Types by Number of Injuries')
plt.show()
