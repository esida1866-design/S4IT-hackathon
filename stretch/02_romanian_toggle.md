# Stretch 2 — Romanian language toggle ⭐ (~10 min)

Add a sidebar switch to flip the dashboard UI between English and Romanian.

## What you'll see
A radio button in the sidebar: 🇬🇧 EN / 🇷🇴 RO. Click RO and the headers, labels and verdicts switch language.

## Where to plug it in
Paste this **near the top** of `app.py`, right after `st.set_page_config(...)`. Then replace the hardcoded English strings further down with `t["key"]` lookups (a few examples below).

## The code

```python
# ------------------------------------------------------------------------------
# STRETCH — language toggle
# ------------------------------------------------------------------------------
# Sidebar radio button to pick language
lang = st.sidebar.radio("🌐 Language", ["🇬🇧 EN", "🇷🇴 RO"], horizontal=True)

# All UI strings live in this dict so we can swap them at once
translations = {
    "🇬🇧 EN": {
        "title": "🌬️ Bucharest Air Quality",
        "subtitle": "Live data from sensors across Bucharest",
        "map_header": "🗺️ Live Air Quality Heatmap",
        "exercise_header": "🏃 Can I exercise outside?",
        "table_header": "📊 All sensors — detailed view",
        "yes": "YES — GO ENJOY IT",
        "mostly_ok": "MOSTLY OK",
        "careful": "BE CAREFUL",
        "not_today": "NOT TODAY",
        "stay_in": "STAY INDOORS",
    },
    "🇷🇴 RO": {
        "title": "🌬️ Calitatea Aerului în București",
        "subtitle": "Date live de la senzori din București",
        "map_header": "🗺️ Hartă Live Calitate Aer",
        "exercise_header": "🏃 Pot face sport afară?",
        "table_header": "📊 Toți senzorii — vedere detaliată",
        "yes": "DA — IEȘI AFARĂ",
        "mostly_ok": "ÎN MARE OK",
        "careful": "FII ATENT",
        "not_today": "NU AZI",
        "stay_in": "RĂMÂI ÎN CASĂ",
    },
}

# `t` is a shortcut to the currently-selected language dict
t = translations[lang]
```

## Then use `t["..."]` in your existing code
Replace these lines (find them in `app.py`):

```python
# Before:
st.subheader("🗺️ Live Air Quality Heatmap")
# After:
st.subheader(t["map_header"])

# Before:
st.subheader("🏃 Can I exercise outside?")
# After:
st.subheader(t["exercise_header"])

# Before (inside TODO 5):
verdict_text = "YES — GO ENJOY IT"
# After:
verdict_text = t["yes"]
```

## Difficulty: ⭐ · Time: ~10 min
