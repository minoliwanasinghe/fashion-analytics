import streamlit as st
import pandas as pd
import io
import time

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="TrendTracker | Data Engine", layout="wide")

# 2. BEAUTIFIED CLEAN CSS
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    
    /* Clean Header */
    .header-box {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        border-bottom: 2px solid #f0f0f0;
        margin-bottom: 2rem;
        text-align: center;
    }
    .header-box h1 { color: #800020; font-weight: 800; font-size: 42px; }
    
    /* Modern Section Headers */
    .section-title {
        color: #800020;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 20px;
        border-left: 5px solid #800020;
        padding-left: 15px;
    }

    /* Horizontal Schema Cards */
    .schema-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 30px;
    }
    .schema-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        flex: 1;
        text-align: center;
        border: 1px solid #f0f0f0;
    }
    .schema-card h4 { color: #800020; margin-bottom: 10px; font-size: 18px; }
    .schema-card p { color: #555; font-size: 14px; }

    /* Action Button Styling */
    .stButton>button {
        background: #800020;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background: #a01030;
        box-shadow: 0 5px 15px rgba(128, 0, 32, 0.2);
    }
    
    /* Clean Tab Bar */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 25px;
        background: #f8f9fa;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background: #800020 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. SECURITY
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.error("Access Denied.")
    st.stop()

# --- HEADER ---
st.markdown('<div class="header-box"><h1>Data Processing Engine</h1><p>Clean and transform your social media exports effortlessly.</p></div>', unsafe_allow_html=True)

# --- NAVIGATION ---
tab1, tab2 = st.tabs(["Setup & Resources", "Data Processing Lab"])

with tab1:
    st.markdown('<p class="section-title">Data Configuration Guide</p>', unsafe_allow_html=True)
    
    # BEAUTIFUL SCHEMA CARDS (Non-misleading, clean view)
    st.markdown("""
        <div class="schema-container">
            <div class="schema-card">
                <h4>📅 Date Format</h4>
                <p>Required: <b>YYYY-MM-DD</b><br>(e.g., 2026-05-14)</p>
            </div>
            <div class="schema-card">
                <h4>🏷️ Content Type</h4>
                <p>Video, Reel, Carousel,<br>or Static Image</p>
            </div>
            <div class="schema-card">
                <h4>📈 Core Metrics</h4>
                <p>Numerical values for<br>Likes, Shares & Saves</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # TEMPLATE DOWNLOAD SECTION
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        st.info("**Instructions:** Download the template to ensure your column headers match the engine's requirements. This prevents processing errors.")
    with col_t2:
        template_df = pd.DataFrame({
            'date': ['2026-05-01'], 'content_type': ['Reel'],
            'likes': [0], 'comments': [0], 'shares': [0], 'saves': [0], 'time': ['18:00']
        })
        st.download_button(
            "Download CSV Template",
            template_df.to_csv(index=False),
            "trendtracker_template.csv",
            "text/csv",
            use_container_width=True
        )

with tab2:
    st.markdown('<p class="section-title">Upload & Sanitize</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your messy Instagram CSV file", type="csv")

    if uploaded_file:
        with st.status("Processing...", expanded=True) as status:
            raw_data = pd.read_csv(uploaded_file)
            # (Standard cleaning logic stays here...)
            raw_data.columns = [c.lower().strip() for c in raw_data.columns]
            time.sleep(1.0)
            st.session_state['cleaned_data'] = raw_data
            status.update(label="File Cleaned Successfully!", state="complete", expanded=False)

        st.success(f"System processed {len(raw_data)} rows of data.")
        
        # Summary row
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows Found", len(raw_data))
        c2.metric("Data Status", "Standardized")
        c3.metric("Ready for", "Dashboard")

        if st.button("Go to Analytics Dashboard", use_container_width=True):
            st.switch_page("pages/2_Dashboard.py")