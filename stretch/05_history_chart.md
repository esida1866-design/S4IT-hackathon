# Stretch 5 — Historical chart (last 24h) ⭐⭐⭐ (~25 min)

Show how PM2.5 changed over the last 24 hours at one selected sensor.

## What you'll see
A new section between the map and the verdict card: a dropdown to pick a sensor, and a line chart showing its PM2.5 over the last day.

## Where to plug it in
**Two parts** — a new helper function in `data_fetcher.py` and a chart block in `app.py`.

### Part A — Add this to the bottom of `data_fetcher.py`

```python
# ------------------------------------------------------------------------------
# STRETCH — fetch historical readings for one sensor
# ------------------------------------------------------------------------------
@st.cache_data(ttl=300)
def get_sensor_history(api_key: str, sensor_id: int, hours: int = 24) -> pd.DataFrame:
    """Fetches last N hours of readings for one OpenAQ sensor."""
    from datetime import timedelta                      # used to compute "N hours ago"

    try:
        headers = {"X-API-Key": api_key}
        # Build ISO-formatted date range
        now = datetime.utcnow()
        start = (now - timedelta(hours=hours)).isoformat() + "Z"
        end = now.isoformat() + "Z"

        # Hourly measurements endpoint
        response = requests.get(
            f"{API_BASE_URL}/sensors/{sensor_id}/measurements/hourly",
            headers=headers,
            params={
                "datetime_from": start,
                "datetime_to": end,
                "limit": hours,
            },
            timeout=10,
        )
        response.raise_for_status()
        results = response.json().get("results", [])

        # Convert to a simple DataFrame
        rows = [
            {
                "time": r.get("period", {}).get("datetimeFrom", {}).get("utc"),
                "pm25": r.get("value"),
            }
            for r in results
            if r.get("value") is not None
        ]
        return pd.DataFrame(rows)

    except Exception as e:
        print(f"[WARN] History fetch failed: {e}")
        # Return a fake 24h trend so the chart still renders during fallback mode
        from datetime import timedelta
        return pd.DataFrame({
            "time": [(datetime.now() - timedelta(hours=h)).strftime("%H:00") for h in range(24, 0, -1)],
            "pm25": [20 + (h % 7) * 3 for h in range(24)],
        })
```

### Part B — Add this to `app.py`, right after the `st_folium(...)` map render

```python
# ------------------------------------------------------------------------------
# STRETCH — 24-hour history chart
# ------------------------------------------------------------------------------
from data_fetcher import get_sensor_history             # import the new helper

st.subheader("📈 24-hour trend")
st.caption("How did PM2.5 change over the last day at one station?")

# Dropdown to pick a station (uses the same df we already have)
chosen_station = st.selectbox("Pick a station", df["station"].tolist())

# We need the OpenAQ sensor ID — for live data we'd have it in df.
# For sample data we use a placeholder so the chart still renders.
sensor_id_lookup = df.set_index("station").get("sensor_id", pd.Series()).to_dict()
sid = sensor_id_lookup.get(chosen_station, 0)

# Fetch the history (or fake data if API/sample mode)
history_df = get_sensor_history(OPENAQ_API_KEY, sid, hours=24)

if not history_df.empty:
    # st.line_chart is Streamlit's built-in chart — one line of code
    st.line_chart(history_df.set_index("time")["pm25"], height=250)
    # Show a quick summary
    avg_h = round(history_df["pm25"].mean(), 1)
    st.caption(f"24h average at {chosen_station}: **{avg_h} μg/m³**")
else:
    st.info("No historical data available for this sensor.")
```

## How it works
- We add a new cached function that hits OpenAQ's hourly endpoint
- If the API call fails (or we're on sample data), we generate a plausible fake 24h trend so the chart still has something to show
- `st.line_chart` is Streamlit's one-liner chart widget — give it a DataFrame, get a chart

## Difficulty: ⭐⭐⭐ · Time: ~25 min
