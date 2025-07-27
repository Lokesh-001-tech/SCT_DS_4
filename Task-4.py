import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# Step 1: Generate synthetic accident data
np.random.seed(42)
n = 2000
df = pd.DataFrame({
    'time_of_day': np.random.randint(0, 24, size=n),
    'weather': np.random.choice(['Clear', 'Rain', 'Fog', 'Snow', 'Cloudy'], size=n, p=[0.6, 0.2, 0.05, 0.05, 0.1]),
    'road_condition': np.random.choice(['Dry', 'Wet', 'Icy', 'Snowy'], size=n, p=[0.7, 0.2, 0.05, 0.05]),
    'latitude': np.random.uniform(40.0, 41.0, size=n),
    'longitude': np.random.uniform(-74.0, -73.0, size=n),
})
# Define severity: more severe when worsened conditions
df['severity'] = np.where(
    ((df['weather'].isin(['Rain', 'Fog', 'Snow'])) | (df['road_condition'].isin(['Wet', 'Icy', 'Snowy']))) &
    (df['time_of_day'].isin(range(0, 6))),
    'Major',
    'Minor'
)

# Step 2: Plot accidents by time of day
plt.figure(figsize=(10, 5))
sns.countplot(x='time_of_day', data=df, palette='viridis')
plt.title("Accidents by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Step 3: Plot weather conditions during accidents
plt.figure(figsize=(8, 5))
sns.countplot(y='weather', data=df, order=df['weather'].value_counts().index, palette='coolwarm')
plt.title("Accidents by Weather Condition")
plt.xlabel("Count")
plt.ylabel("Weather")
plt.tight_layout()
plt.show()

# Step 4: Plot road conditions during accidents
plt.figure(figsize=(8, 5))
sns.countplot(y='road_condition', data=df, order=df['road_condition'].value_counts().index, palette='mako')
plt.title("Accidents by Road Condition")
plt.xlabel("Count")
plt.ylabel("Road Condition")
plt.tight_layout()
plt.show()

# Step 5: Hotspot Map visualization
sample = df[['latitude', 'longitude']].sample(1000)
map_center = [sample['latitude'].mean(), sample['longitude'].mean()]
acc_map = folium.Map(location=map_center, zoom_start=12)
HeatMap(data=sample.values, radius=8).add_to(acc_map)
acc_map.save("accident_hotspots_map.html")
print("✅ Accident hotspots map saved as 'accident_hotspots_map.html'")

# Step 6 (Optional): Severity vs weather or road
plt.figure(figsize=(8, 5))
sns.countplot(x='weather', hue='severity', data=df, palette='Set2')
plt.title("Severity by Weather Condition")
plt.xlabel("Weather")
plt.ylabel("Count")
plt.legend(title="Severity")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
