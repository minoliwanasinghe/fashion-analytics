import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="TrendTracker Intelligence", layout="wide")

# 2. UI STYLING
def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #FDFDFD; font-family: 'Segoe UI', Helvetica, sans-serif; }
        
        /* Sidebar Styling */
        [data-testid="stSidebarNav"] ul li a span { color: #FFFFFF !important; }
        [data-testid="stSidebar"] { background-color: #2F4F4F !important; }

        /* Centered and Bold Main Header */
        .main-header {
            font-size: 32px; 
            font-weight: 800; 
            color: #800020; 
            text-align: center;
            margin-bottom: 25px;
        }
        
        .sub-header {
            font-size: 22px; font-weight: 700; color: #2F4F4F;
            text-transform: uppercase; margin-top: 20px;
            border-bottom: 2px solid #800020; padding-bottom: 5px;
        }

        /* Executive Strategy Card */
        .strategy-card {
            background-color: #FFFFFF; color: #000000; padding: 25px; 
            border: 1px solid #2F4F4F; border-left: 10px solid #800020;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }

        /* Metric Box Styling */
        div[data-testid="stMetric"] {
            background-color: #F8F9FA; border: 1px solid #DEE2E6; padding: 15px;
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# 3. SECURITY GATEKEEPER
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("AUTHENTICATION REQUIRED: ACCESS DENIED.")
    st.stop()

# 4. DATA CORE
if 'cleaned_data' in st.session_state:
    df = st.session_state['cleaned_data'].copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['day_of_week'] = df['date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)
    
    if 'media_type' in df.columns and 'content_type' not in df.columns:
        df = df.rename(columns={'media_type': 'content_type'})
        
    df['engagement'] = (
        df['likes'].fillna(0) + df['comments'].fillna(0) + 
        df['shares'].fillna(0) + df['saves'].fillna(0)
    )
else:
    st.markdown('<p class="main-header">**PERFORMANCE DASHBOARD**</p>', unsafe_allow_html=True)
    st.error("DATA ERROR: NO SOURCE DETECTED.")
    st.stop()

# 5. DASHBOARD HEADER (Centered and Bold)
st.markdown('<p class="main-header">**BUSINESS PERFORMANCE AUDIT & ANALYTICS**</p>', unsafe_allow_html=True)

# 6. FILTERS
st.markdown('**<u>DATA FILTERS</u>**', unsafe_allow_html=True)
c_f1, c_f2 = st.columns(2)
with c_f1:
    start_date = st.date_input("START DATE", df['date'].min())
with c_f2:
    end_date = st.date_input("END DATE", df['date'].max())

mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
f_df = df.loc[mask]
st.divider()

# 7. PERFORMANCE KPIs
if not f_df.empty:
    best_t = f_df.groupby('content_type')['engagement'].mean().idxmax()
    best_d = f_df.groupby('day_of_week')['engagement'].mean().idxmax()
    avg_e = int(f_df['engagement'].mean())
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("POST COUNT", len(f_df))
    k2.metric("BENCHMARK SCORE", f"{avg_e:,} pts")
    k3.metric("OPTIMAL FORMAT", best_t)
    k4.metric("PEAK WINDOW", best_d)

    st.divider()

    # 8. ANALYTICAL VISUALS
    vl, vr = st.columns(2)
    with vl:
        st.markdown('**<u>POST STYLE PERFORMANCE</u>**', unsafe_allow_html=True)
        avg_chart = f_df.groupby('content_type')['engagement'].mean().sort_values(ascending=False)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        sns.barplot(x=avg_chart.index, y=avg_chart.values, color="#800020", ax=ax1)
        st.pyplot(fig1)

    with vr:
        st.markdown('**<u>BEST TIME TO POST</u>**', unsafe_allow_html=True)
        pivot = f_df.pivot_table(values='engagement', index='content_type', columns='day_of_week', aggfunc='mean').fillna(0)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Reds", ax=ax2)
        st.pyplot(fig2)

    # 9. STRATEGIC INTELLIGENCE (Simple English Instructions)
    st.divider()
    st.markdown('<p class="sub-header">STRATEGIC INTELLIGENCE</p>', unsafe_allow_html=True)
    
    with st.expander("HOW TO USE THIS PAGE"):
        st.markdown("""
        **USER GUIDE:**
        1. **Benchmark Score:** This is your account's past average interaction. Your goal is to post content that scores higher than this number.
        2. **Impact Forecaster:** Use the drop-down menus below to pick a post type and a day. The system will guess how many points that post might get.
        3. **Weekly Roadmap:** Look at the table to see what you should post each day to get the most attention from your followers.
        
        **SIMPLE DEFINITIONS:**
        - **Points (pts):** This is the total number of Likes, Comments, Shares, and Saves on a post.
        - **System Logic:** We look at your past successful posts to calculate which days and styles will work best for your future posts.
        """)

    st.markdown(f"""
    <div class="strategy-card">
        <b style="color:#800020;"><u>EXECUTIVE SUMMARY:</u></b><br><br>
        THE ANALYSIS IDENTIFIES <b>{best_t}</b> AS THE PRIMARY CONTENT ASSET FOR THE <b>{best_d}</b> DEPLOYMENT WINDOW. 
        <b>BOLD EXECUTION</b> OF THIS COMBINATION IS RECOMMENDED TO OPTIMIZE ROI BENCHMARKS.
    </div>
    """, unsafe_allow_html=True)

    c_sim, c_plan = st.columns([1, 1.2])

    with c_sim:
        st.markdown('**<u>IMPACT FORECASTER</u>**', unsafe_allow_html=True)
        p_t = st.selectbox("FORMAT SELECTION", f_df['content_type'].unique())
        p_d = st.selectbox("DAY SELECTION", day_order)
        
        t_w = 1.5 if p_t == best_t else 1.0
        d_w = 1.3 if p_d == best_d else 1.0
        proj_score = int(avg_e * t_w * d_w)
        
        st.metric("PROJECTED IMPACT SCORE", f"{proj_score} PTS", delta=f"{proj_score - avg_e}")
        st.progress(min(proj_score / (avg_e * 3 if avg_e > 0 else 100), 1.0))

    with c_plan:
        st.markdown('**<u>7-DAY DEPLOYMENT ROADMAP</u>**', unsafe_allow_html=True)
        road_data = []
        for d in day_order:
            if d == best_d:
                task, obj = f"**PRIMARY {best_t} DEPLOYMENT**", "REVENUE"
            elif d in ["Saturday", "Sunday"]:
                task, obj = "NARRATIVE ASSET DEPLOYMENT", "TRUST"
            elif d in ["Tuesday", "Thursday"]:
                task, obj = "AUDIENCE INTERACTION LAYER", "RETENTION"
            else:
                task, obj = "EVERGREEN CONTENT CYCLE", "AWARENESS"
            road_data.append({"DAY": d, "STRATEGIC TASK": task, "OBJECTIVE": obj})
        
        st.table(pd.DataFrame(road_data))

    # 10. ARCHIVE
    st.divider()
    with st.expander("VIEW DATASET ARCHIVE"):
        st.dataframe(f_df.sort_values(by='date', ascending=False), use_container_width=True)
else:
    st.warning("NO RESULTS FOUND FOR THE SELECTED PARAMETERS.")