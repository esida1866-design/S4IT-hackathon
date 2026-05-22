# Stretch 1 — Bucharest district filter ⭐ (~10 min)

Add a sidebar dropdown that filters the sensors to just one Bucharest sector.

## What you'll see
A new dropdown appears in the left sidebar. Pick "Sector 3" and only sensors in that area show on the map and in the metrics.

## Where to plug it in
Paste this **right after** the line `df = get_bucharest_air_quality(OPENAQ_API_KEY)` in `app.py` (Section B, near the top).

## The code

```python
# ------------------------------------------------------------------------------
# STRETCH — sidebar district filter
# ------------------------------------------------------------------------------
# Show the sidebar (page_config has it collapsed by default)
st.sidebar.header("🏙️ Filter by district")

# Approximate Bucharest sector centers (lat, lon)
# We assign each sensor to the closest sector based on coordinates
sectors = {
    "All sectors": None,                            # special: no filter
    "Sector 1 (north)": (44.49, 26.07),             # Herastrau, Pipera, Otopeni
    "Sector 2 (north-east)": (44.46, 26.16),        # Pantelimon
    "Sector 3 (east)": (44.42, 26.15),              # Titan
    "Sector 4 (south)": (44.39, 26.13),             # Berceni
    "Sector 5 (south-west)": (44.42, 26.07),        # Cotroceni
    "Sector 6 (west)": (44.43, 26.02),              # Militari, Drumul Taberei
}

# The dropdown widget — returns the user's choice
chosen = st.sidebar.selectbox("District", list(sectors.keys()))

# If the user picked a real sector, filter df to sensors closest to it
if sectors[chosen] is not None:
    target_lat, target_lon = sectors[chosen]
    # Compute squared distance from each sensor to the sector center
    df["_dist"] = (df["lat"] - target_lat) ** 2 + (df["lon"] - target_lon) ** 2
    # Keep only the 3 closest sensors to that sector
    df = df.nsmallest(3, "_dist").drop(columns="_dist").reset_index(drop=True)
    st.sidebar.caption(f"Showing 3 sensors closest to **{chosen}**")
```

## How it works
- `st.sidebar.selectbox` is the same as `st.selectbox` but lives in the sidebar
- We compute distance from each sensor to the chosen sector's center
- `df.nsmallest(3, "_dist")` keeps only the 3 nearest sensors
- The rest of the page (metrics, map, verdict) automatically uses the filtered `df`

## Difficulty: ⭐ · Time: ~10 min
