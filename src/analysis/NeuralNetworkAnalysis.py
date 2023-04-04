import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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

# Select the relevant features for input and output
X = merged_data[["Vol", "HH"]]  # You can add more features to this list
y = merged_data["NUMBER OF PERSONS INJURED"]

# Split the data into training and testing sets (80% for training and 20% for testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create a neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='linear')
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1, verbose=1)

# Evaluate the model on the testing set
test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
print("Test Mean Absolute Error:", test_mae)

# Make predictions
y_pred = model.predict(X_test)

# Compare the predicted values with the true values
for i in range(10):
    print(f"Predicted: {y_pred[i][0]:.2f}, True: {y_test.iloc[i]}")
