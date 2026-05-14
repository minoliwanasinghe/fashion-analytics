import streamlit as st

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="TrendTracker | Secure Login", layout="wide")

# 2. THE DEVELOPER-CONTROLLED USER DATABASE
USER_CREDENTIALS = {
    "Supipi_Admin": "Trend2026!",      
    "Joey_Admin": "JoeyFashion#2026", 
    "admin": "1234",                  
    "Examiner_PU": "Plymouth1095"     
}

# 3. SESSION STATE INITIALIZATION
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 4. LOGIN FUNCTION
def login_page():
    st.markdown("""
        <style>
        .stApp { background-color: #F8F9FA; }
        
        /* Main Login Card Styling */
        div[data-testid="stForm"] {
            background-color: #FFFFFF;
            padding: 40px;
            border-radius: 8px;
            border: 1px solid #E0E0E0;
            border-top: 15px solid #800000; /* Deep Maroon Top Border */
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            max-width: 600px;
            margin: auto;
        }

        /* NEW BUTTON COLOR: Slate Charcoal */
        .stButton>button {
            background-color: #264653;
            color: white;
            font-weight: bold;
            border-radius: 4px;
            height: 3.5em;
            width: 100%;
            border: none;
            transition: 0.3s;
            font-size: 18px;
        }
        .stButton>button:hover {
            background-color: #800000; /* Changes to Maroon on hover */
            color: white;
        }

        /* NEW TITLE COLOR: Crimson Maroon */
        .brand-title { 
            color: #800000; 
            font-size: 7vw; 
            font-weight: 900; 
            text-align: center; 
            margin-top: 40px;
            margin-bottom: 5px;
            line-height: 1.2; 
            letter-spacing: 3px;
            display: block;
            width: 100%;
            text-transform: uppercase;
        }
        
        .instruction-text { 
            color: #455A64; 
            text-align: center; 
            font-size: 20px;
            margin-top: 0px;
            margin-bottom: 40px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header section
    st.markdown('<h1 class="brand-title">TrendTracker Intelligence</h1>', unsafe_allow_html=True)
    st.markdown('<p class="instruction-text"><b>Please enter the username and password given</b></p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        with st.form("login_form"):
            user_input = st.text_input("Username")
            pass_input = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Sign In")

            if login_button:
                if user_input in USER_CREDENTIALS and USER_CREDENTIALS[user_input] == pass_input:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = user_input
                    st.success("Login Successful.")
                    st.switch_page("pages/1_Data_Management.py")
                else:
                    st.error("Invalid Username or Password.")

# 5. AUTHENTICATION LOGIC
if not st.session_state["authenticated"]:
    login_page()
else:
    st.sidebar.markdown(f"**Current User:** {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title("Welcome to TrendTracker")
    if st.button("Proceed to Data Management"):
        st.switch_page("pages/1_Data_Management.py")