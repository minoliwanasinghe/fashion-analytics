import streamlit as st

# 1. Setup - This must be the first Streamlit command
st.set_page_config(
    page_title="Fashion Analytics Login", 
    page_icon="👠",
    layout="centered"
)

# 2. Initialize Session State (This keeps the user logged in as they move between pages)
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 3. Login Interface
if not st.session_state["authenticated"]:
    st.title("🔐 Client Login")
    st.write("Welcome! Please enter your credentials to access your fashion analytics dashboard.")
    
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login", use_container_width=True):
        # Update these credentials as needed for your client
        if username == "admin" and password == "1234":
            st.session_state["authenticated"] = True
            st.success("Login Successful! Redirecting...")
            # This path is case-sensitive and must match your GitHub folder name
            st.switch_page("pages/1_Data_Management.py") 
        else:
            st.error("Invalid credentials. Please try again.")

# 4. Authenticated View (What the user sees after logging in)
else:
    st.title("✅ Welcome back, Admin!")
    st.subheader("What would you like to do today?")
    
    st.info("The navigation menu is now also available on the left sidebar.")

    # Two big buttons for easy navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📂 Upload & Manage Data", use_container_width=True):
            st.switch_page("pages/1_Data_Management.py")
            
    with col2:
        if st.button("📊 View Performance Dashboard", use_container_width=True):
            st.switch_page("pages/2_Dashboard.py")
    
    st.divider()
    
    # Logout Button
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()