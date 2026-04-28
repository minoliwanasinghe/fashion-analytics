import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Analytics Dashboard", layout="wide")

# 2. SECURITY GATEKEEPER
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("🔒 Access Denied. Please login on the Home page.")
    st.image("https://cdn-icons-png.flaticon.com/512/3064/3064155.png", width=100)
    if st.button("Go to Home Page"):
        st.switch_page("Home.py")
    st.stop()

# 3. SMART DATA LOADING (Client-Proof Logic)
# This checks the main folder AND the subfolder so the client doesn't get lost
FILE_NAME = "instagram_data.csv"
SUBFOLDER_PATH = os.path.join("data", FILE_NAME)

if os.path.exists(FILE_NAME):
    DATA_PATH = FILE_NAME # Found in main folder
elif os.path.exists(SUBFOLDER_PATH):
    DATA_PATH = SUBFOLDER_PATH # Found in data/ folder
else:
    st.title("📊 Analytics Dashboard")
    st.error("❌ No data source detected.")
    st.info("""
    **To see results, please choose one:**
    1. Go to **Data Management** and upload your CSV.
    2. Place a file named `instagram_data.csv` in your project folder.
    """)
    st.stop()

# Load the data
df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])

# 4. SIDEBAR FILTERS
st.sidebar.title("Dashboard Controls")
start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

# 5. CORE CALCULATIONS
filtered_df['engagement'] = filtered_df['likes'] + filtered_df['comments'] + filtered_df['shares'] + filtered_df['saves']

# 6. HEADER & REFRESH
st.title("📊 Social Media Analytics Dashboard")

# Professional Sync Button for the Client
if st.button("🔄 Sync New Data"):
    st.cache_data.clear()
    st.rerun()

# 7. SUMMARY METRICS (Maroon Cards)
best_type = filtered_df.groupby('content_type')['engagement'].mean().idxmax()
best_hour = filtered_df.groupby('time')['engagement'].mean().idxmax()

with st.container():
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] {
            font-size: 32px;
            font-weight: bold;
            color: #800020; /* Your Maroon Accent */
        }
        [data-testid="stMetricLabel"] {
            font-size: 16px;
            color: #555555;
        }
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Posts", len(filtered_df))
    col2.metric("Avg Engagement", int(filtered_df['engagement'].mean()))
    col3.metric("Top Format", best_type)
    col4.metric("Peak Time", best_hour)

# 8. VISUALIZATIONS
st.divider()
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'none'

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Engagement by Content Type")
    content_eng = filtered_df.groupby('content_type')['engagement'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots()
    sns.barplot(x=content_eng.index, y=content_eng.values, ax=ax, palette="rocket")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col_right:
    st.subheader("Performance Heatmap")
    pivot = filtered_df.pivot_table(values='engagement', index='content_type', columns='time')
    fig, ax = plt.subplots()
    sns.heatmap(pivot, annot=True, fmt=".0f", ax=ax, cmap="YlGnBu")
    st.pyplot(fig)

# 9. BUSINESS INSIGHTS
st.divider()
row1_col1, row1_col2 = st.columns([1, 2])

with row1_col1:
    st.subheader("💡 Key Insights")
    lowest_type = filtered_df.groupby('content_type')['engagement'].mean().idxmin()
    st.write(f"• **{best_type}s** are outperforming all other formats.")
    st.write(f"• Peak interactions occur at **{best_hour}**.")
    st.write(f"• **{lowest_type}s** are currently underperforming.")

with row1_col2:
    st.subheader("🤖 AI Content Strategy")
    avg_eng = filtered_df['engagement'].mean()
    max_eng = filtered_df['engagement'].max()
    projection = int(((max_eng - avg_eng) / avg_eng) * 100) if avg_eng > 0 else 0

    st.success(f"""
    **Strategic Recommendation:** To maximize reach, prioritize your production budget for **{best_type}s**. 
    Posting during the **{best_hour}** window is projected to increase engagement by **{projection}%**.
    """)