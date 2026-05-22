# Stretch 3 — Sensor deep-dive expander ⭐⭐ (~15 min)

Add a clickable expander per sensor showing its stats vs the city average.

## What you'll see
Below the stations table, one expandable row per sensor. Click "Bucharest-Pantelimon ▾" and you see: its current reading, how it compares to the city average, and whether it's above or below.

## Where to plug it in
Paste this **right after the stations table** in Section E (after the `st.dataframe(...)` block), before `# FOOTER`.

## The code

```python
# ------------------------------------------------------------------------------
# STRETCH — sensor deep-dive expanders
# ------------------------------------------------------------------------------
st.subheader("🔍 Sensor deep-dive")
st.caption("Click a station name to expand and see how it compares to the city average.")

# Loop through every sensor and create an expander for it
for _, row in df.sort_values("pm25").iterrows():
    # Compute the difference from city average
    delta = round(row["pm25"] - avg_pm25, 1)
    # Choose an arrow + color based on whether it's above or below average
    if delta > 0:
        arrow = "⬆️"                              # worse than average (more pollution)
        verdict = f"{abs(delta)} μg/m³ above city average — worse than typical"
    elif delta < 0:
        arrow = "⬇️"                              # better than average
        verdict = f"{abs(delta)} μg/m³ below city average — cleaner than typical"
    else:
        arrow = "➡️"                              # exactly average
        verdict = "Exactly at the city average"

    # The expander itself
    with st.expander(f"{arrow}  {row['station']} — {row['pm25']} μg/m³"):
        # Inside the expander we lay out a 3-column comparison
        c1, c2, c3 = st.columns(3)
        c1.metric("This sensor", f"{row['pm25']} μg/m³")
        c2.metric("City average", f"{avg_pm25} μg/m³")
        c3.metric("Difference", f"{delta:+.1f} μg/m³")
        # And the human-readable verdict line
        st.caption(verdict)
```

## How it works
- `st.expander(label)` creates a collapsed section that opens on click
- We sort sensors cleanest-first so the expanders are in a sensible order
- Inside each expander we reuse `st.metric` and `st.columns` — same building blocks as the top of the page
- `{delta:+.1f}` formats the number with a sign (+ or -) and 1 decimal

## Difficulty: ⭐⭐ · Time: ~15 min
