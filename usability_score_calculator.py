import streamlit as st

def calculate_usability_score(conversion, expected_conversion, time, expected_time, error_rate, support_touch_rate):
    try:
        conversion_factor = min(1, conversion / expected_conversion)
        time_factor = min(1, expected_time / time)
        error_factor = 1 - error_rate
        support_factor = 1 - support_touch_rate
        raw_score = 100 * conversion_factor * time_factor * error_factor * support_factor
        capped_score = min(100, raw_score)
        return round(capped_score, 2)
    except ZeroDivisionError:
        return "Error: Division by zero. Please check your inputs."

st.title("Feature Usability Score Calculator")

# Initialize session state variables at the very start
for var in ["calculated", "base_conversion", "base_time", "base_error_rate", "base_support_touch_rate"]:
    if var not in st.session_state:
        st.session_state[var] = None

st.header("Enter Actual Values:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    conversion = st.number_input("Conversion Rate (%)", min_value=0.0, max_value=100.0, format="%f") / 100
with col2:
    time = st.number_input("Median Time (seconds)", min_value=1.0, format="%f")
with col3:
    error_rate = st.number_input("Error Rate (%)", min_value=0.0, max_value=100.0, format="%f") / 100
with col4:
    support_touch_rate = st.number_input("Support Touch Rate (%)", min_value=0.0, max_value=100.0, format="%f") / 100

st.header("Enter Baseline Values:")
col5, col6 = st.columns(2)
with col5:
    expected_conversion = st.number_input("Expected Conversion Rate (%)", min_value=1.0, max_value=100.0, format="%f") / 100
with col6:
    expected_time = st.number_input("Expected Time (seconds)", min_value=1.0, format="%f")

if st.button("Calculate Usability Score"):
    st.session_state.calculated = True
    st.session_state.base_conversion = conversion
    st.session_state.base_time = time
    st.session_state.base_error_rate = error_rate
    st.session_state.base_support_touch_rate = support_touch_rate

# If calculated, show sliders
if st.session_state.calculated:
    st.header("Adjust Variables with Sliders:")

    slider_conversion = st.slider("Conversion Rate (adjust, %)", 0.0, 100.0, value=st.session_state.base_conversion * 100, step=1.0) / 100
    slider_time = st.slider("Median Time (adjust)", max(1.0, st.session_state.base_time - 30), st.session_state.base_time + 30, value=st.session_state.base_time, step=1.0)
    slider_error_rate = st.slider("Error Rate (adjust, %)", 0.0, 100.0, value=st.session_state.base_error_rate * 100, step=1.0) / 100
    slider_support_touch_rate = st.slider("Support Touch Rate (adjust, %)", 0.0, 100.0, value=st.session_state.base_support_touch_rate * 100, step=1.0) / 100

    usability_score = calculate_usability_score(
        slider_conversion,
        expected_conversion,
        slider_time,
        expected_time,
        slider_error_rate,
        slider_support_touch_rate
    )

    # Color-coded score display
    if usability_score >= 80:
        st.success(f"Excellent Usability Score: {usability_score}")
    elif 50 <= usability_score < 80:
        st.warning(f"Moderate Usability Score: {usability_score}")
    else:
        st.error(f"Poor Usability Score: {usability_score}")