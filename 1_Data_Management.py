import streamlit as st
import pandas as pd
import os
import io

st.set_page_config(page_title="Data Management", layout="wide")

# 1. SECURITY GATEKEEPER
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("🔒 Access Denied. Please login on the Home page.")
    st.stop()

st.title("📂 Data Management & Cleaning")
st.write("Upload your raw Instagram data here. The system will automatically clean and format it for the dashboard.")

# --- PART A: DOWNLOAD TEMPLATE SECTION ---
st.subheader("1. Get the Template")
st.write("If you don't have a dataset yet, download this template to see the required format.")

# Create a sample template in memory
template_data = {
    'date': ['2026-04-01', '2026-04-02'],
    'content_type': ['Reel', 'Image'],
    'likes': [100, 50],
    'comments': [10, 5],
    'shares': [20, 5],
    'saves': [30, 10],
    'time': ['18:00', '09:00']
}
template_df = pd.DataFrame(template_data)

# Convert dataframe to CSV for download
csv_buffer = io.StringIO()
template_df.to_csv(csv_buffer, index=False)
st.download_button(
    label="📥 Download CSV Template",
    data=csv_buffer.getvalue(),
    file_name="instagram_template.csv",
    mime="text/csv"
)

st.divider()

# --- PART B: UPLOAD & AUTOMATIC CLEANING ---
st.subheader("2. Upload & Process Data")
uploaded_file = st.file_uploader("Choose your Instagram CSV file", type="csv")

if uploaded_file is not None:
    # Read the raw data
    raw_data = pd.read_csv(uploaded_file)
    
    st.info("🔄 Processing and cleaning your data...")
    
    try:
        # --- THE CLEANING LAYER ---
        # 1. Standardize column names (Lowercase and strip spaces)
        raw_data.columns = [c.lower().strip() for c in raw_data.columns]
        
        # 2. Handle missing values (Fill empty numbers with 0)
        numeric_cols = ['likes', 'comments', 'shares', 'saves']
        for col in numeric_cols:
            if col in raw_data.columns:
                raw_data[col] = pd.to_numeric(raw_data[col], errors='coerce').fillna(0)
        
        # 3. Standardize Date format
        if 'date' in raw_data.columns:
            raw_data['date'] = pd.to_datetime(raw_data['date']).dt.strftime('%Y-%m-%d')
            
        # 4. Standardize Content Types (Capitalize first letter)
        if 'content_type' in raw_data.columns:
            raw_data['content_type'] = raw_data['content_type'].str.capitalize()

        # --- SAVING THE CLEANED DATA ---
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Save to the specific paths the Dashboard looks for
        # We save it to both locations to be safe!
        raw_data.to_csv("data/instagram_data.csv", index=False)
        raw_data.to_csv("instagram_data.csv", index=False)
        
        st.success("✅ Data Cleaned & Synchronized Successfully!")
        
        # Show a preview of the cleaned data
        st.write("### Data Preview (Cleaned)")
        st.dataframe(raw_data.head(5), use_container_width=True)
        
        if st.button("📊 View Dashboard"):
            st.switch_page("pages/2_Dashboard.py")
            
    except Exception as e:
        st.error(f"❌ Error cleaning data: {e}")
        st.warning("Please ensure your file matches the template headers.")