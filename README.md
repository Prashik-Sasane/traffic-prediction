# Delhi Traffic Prediction  & OpenStreetMap

A machine learning-powered system to predict travel time. It visualizes live congestion, stop-to-stop delay, and optimal routes using interactive maps and charts.

---

##  Project Description

This project leverages Large Language Models (LLMs) via Groq to enhance the experience of travel time prediction and traffic insights across Delhi. Using curated datasets, it integrates predictive modeling with an interactive Streamlit dashboard, featuring Folium-based maps, real-time travel estimations, and intuitive route visualizations for a smoother and smarter user experience.

<img width="1279" height="628" alt="Screenshot (120)" src="https://github.com/user-attachments/assets/f9da63d5-e1c8-4033-9392-5246c1982b2d" />



---

##  Data Preprocessing & Feature Engineering

All GTFS `.txt` files were processed using pandas in a Jupyter notebook:

###  Steps Involved:
1. **Merged `stop_times.txt` with `stops.txt`** to get latitude/longitude and timestamps.
2. **Sorted by `trip_id` and `stop_sequence`** to ensure sequential travel.
3. **Calculated `travel_time_sec`** between consecutive stops.
4. **Extracted time features**: hour of day, service type (`weekday`, `saturday`, etc.).
5. **Merged with `trips.txt`** to get `route_id`, `direction_id`, and shape ID.
6. **Handled anomalies** like missing values and duplicated trips.
7. **Saved the final DataFrame** as `gtfs_cleaned.csv`.

###  Main Cleaned File: `gtfs_cleaned.csv`
| Feature               | Description                         |
|------------------------|-------------------------------------|
| trip_id               | Unique trip reference               |
| stop_sequence         | Order of stop in trip               |
| arrival_time / dep.   | Timestamps from stop_times.txt      |
| stop_lat / stop_lon   | From stops.txt                      |
| travel_time_sec       | Time between current and next stop  |
| direction_id          | Direction (0 or 1)                  |
| service_id            | weekday/weekend/saturday            |
| hour                  | Extracted from time for patterning  |
| shape_dist_traveled   | Distance covered on shape route     |

###  Libraries Used (Preprocessing):
```
import pandas as pd
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
```
---

##  Streamlit Dashboard

<h3>Left Panel:</h3> Trip planner (source, destination, transport mode, traffic toggle) + LLM Travel Plan.

<h3>Right Panel:</h3> Interactive map showing the selected route.

An interactive UI for users to:

- Select source and destination 
- Predict travel time using trained ML model and LLM advisory 
- View  the routes  on **Folium (OpenStreetMap)**
- Display signal points and their status
- Option for selecting mode of transport 

###  Dashboard Features:

| Feature | Description |
|--------|-------------|
| **Folium Map** | OpenStreetMap centered on Delhi |
| **Stop Info** | Hover to view arrival/departure time |
| **Prediction Box** | Select source → destination → plan |
| **TomTom Routing API** | Provides optimized routes, travel time, distance, and real-time traffic delays |
| **OpenWeather API** | Fetches temperature and weather conditions for the journey |
| **LLM(groq) insights** | Generates a natural language summary with:
                            • Travel time & distance
                            • Expected traffic congestion hotspots
                            • Weather impact
                            • Suggestions (e.g., leave early, precautions) |
### Libraries Used (Dashboard):
```
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import pandas as pd
from dotenv import load_dotenv

# APIs

from services.tomtom_service import geocode_tomtom, route_tomtom
(https://developer.tomtom.com/)

from services.weather_service import weather_onecall
(https://openweathermap.org/)

from services.llm_service import ask_llm
(https://console.groq.com/home)

```

---
## Installation setup 
```
# 1. Clone the repository
git clone https://github.com/SamIeer/traffic-prediction.git
cd traffic-prediction

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter Notebook (if applicable)
jupyter notebook
```

##  Docker Support

You can containerize and deploy the app using Docker:

```###  Dockerfile
docker build -t delhi-traffic-app .
docker run -p 8501:8501 delhi-traffic-app 
```
