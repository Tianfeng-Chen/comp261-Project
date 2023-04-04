import pandas as pd
import numpy as np
import tensorflow as tf

# Load the datasets
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

# Calculate correlation using TensorFlow
# You may choose which columns you want to analyze. In this example, I chose "NUMBER OF PERSONS INJURED" and "VOL"
num_injured = merged_data["NUMBER OF PERSONS INJURED"].values
traffic_vol = merged_data["Vol"].values

# Convert the data to TensorFlow tensors
injured_tensor = tf.convert_to_tensor(num_injured, dtype=tf.float32)
traffic_vol_tensor = tf.convert_to_tensor(traffic_vol, dtype=tf.float32)

# Normalize the tensors
injured_norm = tf.nn.l2_normalize(injured_tensor, axis=-1, epsilon=1e-12, name=None)
traffic_vol_norm = tf.nn.l2_normalize(traffic_vol_tensor, axis=-1, epsilon=1e-12, name=None)

# Calculate the correlation coefficient using the dot product of the normalized tensors
correlation_coefficient = tf.tensordot(injured_norm, traffic_vol_norm, axes=1).numpy()

print("Correlation Coefficient:", correlation_coefficient)
