import streamlit as st

# 1. Setup
st.set_page_config(page_title="Fashion Analytics Login", layout="centered")

# 2. Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 3. Login Logic
if not st.session_state["authenticated"]:
    st.title("🔐 Client Login")
    st.write("Welcome! Please enter your credentials to access the analytics suite.")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Replace 'admin' and '1234' with your desired credentials
        if username == "admin" and password == "1234":
            st.session_state["authenticated"] = True
            st.success("Login Successful! Redirecting...")
            
            # --- THE FIX ---
            # Ensure this path matches your folder structure exactly
            st.switch_page("pages/1_Data_Management.py") 
        else:
            st.error("Invalid credentials")
else:
    # 4. What the user sees AFTER logging in
    st.title("✅ Welcome back, Admin!")
    st.success("You are successfully logged in.")
    
    # Quick Navigation Buttons for Better UX
    col1, col2 = st.columns(2)
    with col1:
        # Corrected path for the Data Management page
        if st.button("📂 Upload New Data"):
            st.switch_page("pages/1_Data_Management.py")
    with col2:
        # Corrected path for the Dashboard page
        if st.button("📊 View Dashboard"):
            st.switch_page("pages/2_Dashboard.py")
    
    st.divider()
    
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()