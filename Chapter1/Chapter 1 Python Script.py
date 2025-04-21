# preprocess.py
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load dataset
df = pd.read_csv("traffic.csv")
df.dropna(inplace=True)

# Encode protocol as numeric
df['Protocol'] = df['Protocol'].astype('category').cat.codes

# Normalize numeric columns
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df.select_dtypes(include='number')))

df_scaled.to_csv("processed_traffic.csv", index=False)
print("✅ Preprocessing complete. Output saved to processed_traffic.csv")


# train_model.py
import pandas as pd
from sklearn.ensemble import IsolationForest

# Load preprocessed data
data = pd.read_csv("processed_traffic.csv")

# Train Isolation Forest model
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(data)

# Predict anomalies
data['anomaly'] = model.predict(data)

data.to_csv("anomaly_results.csv", index=False)
print("✅ Anomaly detection complete. Results saved to anomaly_results.csv")


# visualize.py
import pandas as pd
import matplotlib.pyplot as plt

# Load anomaly results
results = pd.read_csv("anomaly_results.csv")

plt.figure(figsize=(12,6))
plt.plot(results.index, results.iloc[:, 0], label='Traffic Pattern')

# Highlight anomalies
anomalies = results[results['anomaly'] == -1]
plt.scatter(anomalies.index, anomalies.iloc[:, 0], color='red', label='Anomalies')

plt.title("Anomaly Detection in Open5GS Traffic")
plt.xlabel("Index")
plt.ylabel("Normalized Metric")
plt.legend()
plt.grid(True)
plt.savefig("anomaly_plot.png")
plt.show()
print("✅ Visualization complete. Saved to anomaly_plot.png")
