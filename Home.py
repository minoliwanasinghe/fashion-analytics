import streamlit as st

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="TrendTracker | Brand Access", layout="wide")

# 2. UI STYLE DEFINITION
def apply_home_style():
    st.markdown("""
        <style>
        /* Main background */
        .stApp {
            background-color: #FAFAFA;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        
        /* Sidebar Visibility Fix */
        [data-testid="stSidebar"] {
            background-color: #2D2D2D !important;
        }
        [data-testid="stSidebarNav"] ul li a span {
            color: #FFFFFF !important;
            font-weight: 500;
        }
        [data-testid="stSidebarNav"] ul li div[data-selected="true"] {
            background-color: #800020 !important;
            border-radius: 5px;
        }

        /* Hero Section - Fix for Screenshot 2026-05-02 at 16.25.31.jpg */
        /* Forces the container to be invisible/transparent */
        .hero-container {
            padding: 10px;
            text-align: center;
            background-color: transparent !important; 
            border: none !important;
            box-shadow: none !important;
            margin-top: 20px;
        }
        
        .main-title {
            font-size: 55px;
            font-weight: 800;
            color: #800020;
            margin-bottom: 0px;
        }

        /* Customer Login Card */
        .login-card {
            max-width: 450px;
            margin: 0 auto;
            padding: 40px;
            background: white;
            border: 1px solid #E0E0E0;
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.05);
        }

        /* High-contrast Labels for Customer Login */
        label[data-testid="stWidgetLabel"] p {
            color: #2D2D2D !important;
            font-weight: 700 !important;
            font-size: 16px !important;
        }

        /* Maroon Primary Button */
        .stButton>button {
            background-color: #800020;
            color: white;
            border-radius: 25px;
            width: 100%;
            border: none;
            padding: 12px;
            font-weight: 600;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #A52A2A;
            color: #FFD700;
        }
        </style>
    """, unsafe_allow_html=True)

apply_home_style()

# 3. CONTENT LAYOUT
st.markdown("""
    <div class="hero-container">
        <p class="main-title">TrendTracker</p>
        <p class="sub-title" style="color: #444444; font-size: 20px;">Premium Fashion Analytics & Insights</p>
    </div>
""", unsafe_allow_html=True)

# 4. CUSTOMER LOGIN LOGIC
col1, col2, col3 = st.columns([1, 1.8, 1])

with col2:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.subheader("🔑 Brand Access")
    st.info("Please enter the credentials provided by your account manager.")
    
    username = st.text_input("Username", placeholder="e.g. joey_clothing")
    password = st.text_input("Password", type="password", placeholder="••••")
    
    if st.button("Get Started"):
        # The credentials you provide to your customers
        if username == "admin" and password == "1234":
            st.session_state["authenticated"] = True
            st.success("✨ Access Granted. Loading insights...")
            # Still landing on Data Management so they can check their data
            st.switch_page("pages/1_Data_Management.py") 
        else:
            st.error("❌ Invalid credentials. Please contact support.")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. FOOTER
st.markdown("<br><br>", unsafe_allow_html=True) 
st.divider()
st.caption("© 2026 TrendTracker | Data Science Final Project | NSBM Green University")