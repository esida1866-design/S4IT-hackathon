# Stretch 4 — "Notify me" email form ⭐⭐ (~15 min)

Add a mock email-signup form for bad-air alerts.

## What you'll see
A form below the verdict card. Type your email, click Subscribe, and a friendly message confirms (in-memory only — nothing is actually sent).

## Where to plug it in
Paste this **right after the `st.info(...)` tip line** in Section D (where the verdict card lives), before `# SECTION E — STATIONS TABLE`.

## The code

```python
# ------------------------------------------------------------------------------
# STRETCH — "Notify me" signup form
# ------------------------------------------------------------------------------
st.subheader("📧 Get bad-air alerts")
st.caption("We'll email you when PM2.5 crosses 35 μg/m³ in Bucharest. (Mock form — no email is actually sent.)")

# Use Streamlit's session_state to remember subscriptions across reruns
# (the script reruns every time something changes, but session_state survives)
if "subscribers" not in st.session_state:
    st.session_state.subscribers = []

# st.form groups widgets so they only submit together when the button is clicked
# (without this, every keystroke would trigger a full page rerun)
with st.form("notify_form", clear_on_submit=True):
    # Two columns: input on the left, button on the right
    col_email, col_btn = st.columns([3, 1])

    with col_email:
        # The text input — returns whatever the user typed
        email = st.text_input(
            "Your email",
            placeholder="you@example.com",
            label_visibility="collapsed",      # hide the label, the subheader is enough
        )

    with col_btn:
        # The submit button — must live inside the st.form block
        submitted = st.form_submit_button("Subscribe")

# Handle the submission AFTER the form block ends
if submitted:
    if "@" in email and "." in email:
        # Naïve email validation: must contain @ and .
        st.session_state.subscribers.append(email)
        st.success(f"✅ Thanks! We'll alert {email} when air quality drops.")
    else:
        st.error("⚠️ That doesn't look like a valid email. Try again.")

# Show how many people have "subscribed" this session
if st.session_state.subscribers:
    st.caption(f"👥 {len(st.session_state.subscribers)} subscriber(s) so far this session.")
```

## How it works
- `st.session_state` is Streamlit's in-memory dict that survives reruns
- `st.form(...)` batches widgets so they don't re-trigger the page on every keystroke
- `clear_on_submit=True` empties the email box after each submit
- We don't actually send email — this is a mock. To send real email you'd need an SMTP service like SendGrid or Resend

## Difficulty: ⭐⭐ · Time: ~15 min
