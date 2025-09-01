import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="secrets.env")
TOMTOM_KEY = os.getenv("TOMTOM_API_KEY")

def geocode_tomtom(query: str, country="IN"):
    """Geocode a location name into (lat, lon) using TomTom API."""
    url = f"https://api.tomtom.com/search/2/geocode/{requests.utils.quote(query)}.json"
    params = {"key": TOMTOM_KEY, "limit": 1, "countrySet": country}

    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        js = r.json()
        if js.get("results"):
            pos = js["results"][0]["position"]
            return float(pos["lat"]), float(pos["lon"])
    except requests.RequestException as e:
        print(f"❌ Geocoding error: {e}")
    return None


def route_tomtom(start_lat, start_lon, end_lat, end_lon, mode="car", traffic=True):
    """Get route summary + polyline points from TomTom Routing API."""
    coord_str = f"{start_lat},{start_lon}:{end_lat},{end_lon}"
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{coord_str}/json"
    params = {
        "key": TOMTOM_KEY,
        "travelMode": mode,
        "traffic": str(traffic).lower(),
        "routeRepresentation": "polyline",
    }

    try:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        js = r.json()
        routes = js.get("routes", [])
        if not routes:
            return None

        best = routes[0]
        summary = best.get("summary", {})

        # Gather all points along the route
        points = []
        for leg in best.get("legs", []):
            for p in leg.get("points", []):
                points.append((p["latitude"], p["longitude"]))

        return {
            "points": points,
            "length_m": summary.get("lengthInMeters"),
            "time_s": summary.get("travelTimeInSeconds"),
            "delay_s": summary.get("trafficDelayInSeconds", 0),
            "departureTime": summary.get("departureTime"),
            "arrivalTime": summary.get("arrivalTime"),
        }
    except requests.RequestException as e:
        print(f"❌ Routing error: {e}")
        return None
