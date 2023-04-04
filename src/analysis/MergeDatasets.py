import pandas as pd
import numpy as np

# Preprocessing and merging the datasets
collision_data = pd.read_csv("collision_data.csv")
traffic_volume = pd.read_csv("traffic_volume.csv")

# Preprocess the data
collision_data["CRASH DATE"] = pd.to_datetime(collision_data["CRASH DATE"])
collision_data["CRASH HOUR"] = collision_data["CRASH DATE"].dt.hour
collision_data["CRASH DAY"] = collision_data["CRASH DATE"].dt.day
collision_data["CRASH MONTH"] = collision_data["CRASH DATE"].dt.month
collision_data["CRASH YEAR"] = np.where(collision_data["CRASH DATE"].dt.year > 2021,
                                        collision_data["CRASH DATE"].dt.year,
                                        np.nan)
collision_data["STREET"] = np.where(collision_data["CROSS STREET NAME"] != "Unspecified",
                                    collision_data["CROSS STREET NAME"].str.split().str[1:].str.join(' '),
                                    collision_data["ON STREET NAME"])
collision_data["STREET"] = collision_data["STREET"].str.lower().str.strip()

# Convert traffic_volume data columns to the appropriate data types
traffic_volume["YR"] = np.where(traffic_volume["Yr"].astype(int) > 2021,
                                traffic_volume["Yr"].astype(int),
                                np.nan)
traffic_volume["M"] = traffic_volume["M"].astype(int)
traffic_volume["D"] = traffic_volume["D"].astype(int)
traffic_volume["HH"] = traffic_volume["HH"].astype(int)
traffic_volume["Street"] = traffic_volume["street"].str.lower()

# Merge the datasets
merged_data = pd.merge(
    collision_data,
    traffic_volume,
    left_on=["CRASH YEAR", "CRASH MONTH", "CRASH DAY", "CRASH HOUR", "STREET"],
    right_on=["YR", "M", "D", "HH", "Street"],
    how="inner",
)

print("Merged data shape:", merged_data.shape)
print("Unique values in collision_data:", collision_data["BOROUGH"].unique())
print("Unique values in traffic_volume:", traffic_volume["Boro"].unique())
print("Unique years in collision_data:", collision_data["CRASH YEAR"].unique())
print("Unique years in traffic_volume:", traffic_volume["YR"].unique())
