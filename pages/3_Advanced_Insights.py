
import streamlit as st

# THIS MUST BE THE FIRST THING ON THE PAGE
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("🔒 Access Denied. Please login on the Home page.")
    st.image("https://cdn-icons-png.flaticon.com/512/3064/3064155.png", width=100) # Lock icon
    if st.button("Go to Home Page"):
        st.switch_page("Home.py")
    st.stop() # This kills the script right here so no charts load


import streamlit as st

# 1. SECURITY CHECK
# Ensures no one can access this page without logging in through Home.py
if "authenticated" not in st.session_state:
    st.warning("Please login on the Home page first.")
    st.stop()

# 2. PAGE CONFIGURATION
st.set_page_config(page_title="Advanced Insights", layout="wide")

st.title("📈 Power BI Executive Overview")
st.write("""
This page integrates high-level Business Intelligence (BI) for deep-trend analysis. 
While the Python dashboard focuses on real-time metrics, this Power BI report 
handles complex historical data relationships.
""")

st.divider()

# 3. EMBEDDING LOGIC
# Replace the URL below with your actual "Publish to Web" link from Power BI
# To get this: Power BI Service > File > Embed Report > Publish to Web
power_bi_url = "https://app.powerbi.com/view?r=YOUR_REAL_EMBED_LINK_HERE"

# Creating a professional container for the dashboard
with st.container():
    # We use an iframe component to display the Power BI report
    # We set scrolling=True so users can navigate multiple Power BI tabs
    st.components.v1.iframe(power_bi_url, height=800, scrolling=True)

# 4. TECHNICAL EXPLANATION (For your Viva/Presentation)
with st.expander("ℹ️ About this Integration"):
    st.info("""
    **Data Science Architecture:**
    - **Frontend:** Streamlit (Python)
    - **BI Layer:** Power BI Embedded
    - **Logic:** This integration demonstrates a 'Unified Analytics Interface,' 
      allowing businesses to see automated Python-generated recommendations 
      alongside enterprise-grade BI visuals.
    """)

# 5. FOOTER
st.caption("Fashion Analytics SaaS v1.0 | Integrated BI Module")