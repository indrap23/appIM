import streamlit as st
from utils import init_session_state, login_user

# --- PAGE CONFIGURATION ---
# Use st.set_page_config() as the first Streamlit command.
st.set_page_config(
    page_title="Sistem Inventarisasi Aset LMAN",
    page_icon="🏢",
    layout="centered"
)

# --- INITIALIZE SESSION STATE ---
# This function from utils.py will set up all the necessary data
# in st.session_state if it's not already there.
init_session_state()

# --- LOGIN LOGIC ---
# If the user is already logged in, show a welcome message and links to their dashboards.
if st.session_state.get('logged_in'):
    st.success(f"Anda telah login sebagai **{st.session_state.user_info['name']}**.")
    st.markdown("---")
    
    user_role = st.session_state.user_info['role']
    assigned_roles = st.session_state.user_info.get('assigned_roles', [])

    st.write("### Navigasi Cepat:")
    
    # Show appropriate links based on user role(s)
    if user_role == 'admin':
        st.page_link("pages/1_Admin_Panel.py", label="Buka Admin Panel", icon="👑")
    
    if 'petugas' in assigned_roles:
        st.page_link("pages/2_Petugas_Dashboard.py", label="Buka Dashboard Petugas", icon="👷‍♂️")
        
    if 'verifikator' in assigned_roles:
        st.page_link("pages/3_Verifikator_Dashboard.py", label="Buka Dashboard Verifikator", icon="✅")

    if st.button("Logout"):
        # Reset session state on logout
        for key in list(st.session_state.keys()):
            if key not in ['users_db', 'petugas_db', 'verifikator_db', 'admin_db']:
                del st.session_state[key]
        st.rerun()

# If the user is not logged in, show the login form.
else:
    # --- LOGIN INTERFACE ---
    st.markdown(
        """
        <div style="text-align: center;">
            <div style="display: inline-block; background-color: #E5E7EB; padding: 1rem; border-radius: 9999px; margin-bottom: 1rem;">
                <svg class="w-8 h-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="width: 2rem; height: 2rem; color: #4B5563;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
            </div>
            <h1 style="font-size: 1.875rem; font-weight: bold; color: #1F2937;">Sistem Inventarisasi Aset</h1>
            <p style="color: #6B7280;">Lembaga Manajemen Aset Negara</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    with st.form("login_form", border=False):
        email = st.text_input(
            "Email", 
            placeholder="admin@lman.go.id",
            help="Coba: admin@lman.go.id atau user@lman.go.id"
        )
        submitted = st.form_submit_button("Login", use_container_width=True, type="primary")

        if submitted:
            if login_user(email):
                st.rerun() # Rerun to show the logged-in view
            else:
                st.error("Pengguna tidak ditemukan. Silakan coba lagi.")
    
    st.info("""
    **Untuk Demo:**
    - Email Admin: `admin@lman.go.id`
    - Email User (Petugas & Verifikator): `user@lman.go.id`
    - Email Petugas: `ani@lman.go.id`
    - Email Verifikator: `citra@lman.go.id`
    """)
streamlit_app.py
