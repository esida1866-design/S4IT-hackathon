# ==============================================================================
# data_fetcher.py — handles the API call + caching + fallback
# ==============================================================================
# This file is fully written for you. You do NOT edit anything here.
# It exists so app.py stays focused on the UI.
#
# What this file does:
#   1. Calls OpenAQ API v3 to get current PM2.5 readings for Bucharest
#   2. Caches the result for 5 minutes so we don't hammer the API
#   3. Falls back to sample_data.csv if the API is down or returns nothing
#
# OpenAQ v3 needs TWO calls:
#   1. /v3/locations           → list of sensor stations near Bucharest
#   2. /v3/sensors/{id}/measurements → latest reading for each station
# ==============================================================================

import requests                                  # For HTTP calls to the OpenAQ API
import pandas as pd                              # For tabular data
import streamlit as st                           # For the @st.cache_data decorator
from datetime import datetime                    # For timestamping the data
import os                                        # For checking if the fallback CSV exists


# ------------------------------------------------------------------------------
# CONFIGURATION — constants used by the API call
# ------------------------------------------------------------------------------
BUCHAREST_LAT = 44.4268                          # Latitude of Bucharest center
BUCHAREST_LON = 26.1025                          # Longitude of Bucharest center
SEARCH_RADIUS_METERS = 25000                     # 25 km radius (OpenAQ's max)
API_BASE_URL = "https://api.openaq.org/v3"      # OpenAQ v3 base URL
PM25_PARAMETER_ID = 2                            # OpenAQ's ID for PM2.5
FALLBACK_CSV_PATH = "sample_data.csv"            # Local CSV used if API fails


# ------------------------------------------------------------------------------
# MAIN FUNCTION — called by app.py
# ------------------------------------------------------------------------------
# @st.cache_data(ttl=300) tells Streamlit:
#   "Remember the result for 300 seconds (5 minutes). If anyone calls this
#    function with the same arguments in that window, return the cached result
#    instead of doing real work."
# This is why the dashboard feels instant on re-renders.
@st.cache_data(ttl=300)
def get_bucharest_air_quality(api_key: str) -> pd.DataFrame:
    """Fetches latest PM2.5 readings for Bucharest. Falls back to CSV on failure."""

    try:
        headers = {"X-API-Key": api_key}         # OpenAQ wants the key in this header

        # ----- STEP 1: List sensor locations near Bucharest -----
        params = {
            "coordinates": f"{BUCHAREST_LAT},{BUCHAREST_LON}",  # search center
            "radius": SEARCH_RADIUS_METERS,                      # 25 km
            "parameters_id": PM25_PARAMETER_ID,                  # only PM2.5 sensors
            "limit": 50,                                          # cap results
        }

        response = requests.get(
            f"{API_BASE_URL}/locations",         # /v3/locations endpoint
            headers=headers,
            params=params,
            timeout=10,                          # give up after 10s
        )
        response.raise_for_status()              # raises if HTTP status is 4xx/5xx

        locations = response.json().get("results", [])  # list of location dicts

        if not locations:
            # API returned successfully but with no Bucharest sensors — treat as failure
            raise ValueError("API returned no Bucharest sensors")

        rows = []                                # we'll fill this with one dict per sensor

        # ----- STEP 2: For each location, fetch the latest measurement -----
        for location in locations:
            location_id = location.get("id")     # unique ID for this location
            station_name = location.get("name", "Unknown")
            coords = location.get("coordinates") or {}
            lat = coords.get("latitude")
            lon = coords.get("longitude")

            # Skip incomplete records
            if not location_id or lat is None or lon is None:
                continue

            # Find the PM2.5 sensor inside this location (each location can have
            # several sensors measuring different parameters — we only want PM2.5)
            pm25_sensor_id = None
            for sensor in location.get("sensors", []):
                parameter = sensor.get("parameter", {})
                if parameter.get("id") == PM25_PARAMETER_ID:
                    pm25_sensor_id = sensor.get("id")
                    break

            if not pm25_sensor_id:
                continue                          # no PM2.5 sensor here, move on

            # Fetch the most recent reading from this sensor
            try:
                latest_response = requests.get(
                    f"{API_BASE_URL}/sensors/{pm25_sensor_id}/measurements",
                    headers=headers,
                    params={"limit": 1},          # only the newest reading
                    timeout=5,
                )
                latest_response.raise_for_status()
                measurements = latest_response.json().get("results", [])

                if not measurements:
                    continue                      # no reading available

                pm25_value = measurements[0].get("value")  # the actual number

                if pm25_value is None or pm25_value < 0:
                    continue                      # skip bad readings

                # Build a row dict — this becomes one row in the final DataFrame
                rows.append({
                    "station": station_name,
                    "lat": lat,
                    "lon": lon,
                    "pm25": round(pm25_value, 1),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "source": "OpenAQ Live",
                })

            except Exception as inner_e:
                # One sensor failing shouldn't stop the rest
                print(f"[INFO] Skipping sensor {pm25_sensor_id}: {inner_e}")
                continue

        # If we collected at least one good reading, return them as a DataFrame
        if rows:
            return pd.DataFrame(rows)
        else:
            raise ValueError("No valid sensor readings in API response")

    except Exception as e:
        # ANY failure above lands here — print the reason and fall back to CSV
        print(f"[WARN] OpenAQ API failed: {e}. Using sample data fallback.")

        if os.path.exists(FALLBACK_CSV_PATH):
            df = pd.read_csv(FALLBACK_CSV_PATH)
            df["source"] = "Sample (offline)"
            df["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return df

        # If even the CSV is missing, return an empty DataFrame with the right columns
        return pd.DataFrame(columns=["station", "lat", "lon", "pm25", "last_updated", "source"])
