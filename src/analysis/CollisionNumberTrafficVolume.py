import pandas as pd
import requests
from scipy.stats import pearsonr
import json

# load collision data from local file
data = []
with open('collision_data.json', 'r') as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError:
            continue
collision_data = pd.DataFrame(data)

# extract street name from on_street_name, off_street_name, and cross_street_name columns
collision_data['street_name'] = collision_data['on_street_name'].fillna('') + ' & ' + collision_data['off_street_name'].fillna('') + ' & ' + collision_data['cross_street_name'].fillna('')
collision_data['street_name'] = collision_data['street_name'].str.replace(' &  & ', ' & ').str.strip('& ')

# validate that the street_name column is present in the collision data
if 'street_name' not in collision_data.columns:
    missing_columns = {'street_name'}
    raise ValueError(f"Missing required columns in collision data: {missing_columns}")

# filter and group collision data by street name
collision_data = collision_data[['street_name', 'borough']].groupby('street_name').count().reset_index()
collision_data.rename(columns={'borough': 'collision_count'}, inplace=True)

# API request to load traffic volume data
url = "https://data.cityofnewyork.us/resource/7ym2-wayt.json"
params = {'$select': 'street_name, SUM(aadt)', '$group': 'street_name', '$order': 'street_name ASC'}
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code != 200:
    raise Exception(f"Request failed with status code {response.status_code}")

try:
    traffic_data = pd.read_json(response.content.decode('utf-8'))
except ValueError:
    # If there's an error reading the JSON, try to decode it as UTF-16
    traffic_data = pd.read_json(response.content.decode('utf-16'))

# merge collision and traffic volume data
merged_data = pd.merge(collision_data, traffic_data, on='street_name', how='inner')

# calculate Pearson correlation coefficient and p-value
corr, p_value = pearsonr(merged_data['sum_aadt'], merged_data['collision_count'])

# print the results
print("Pearson correlation coefficient:", corr)
print("p-value:", p_value)

