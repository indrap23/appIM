import streamlit as st
import pandas as pd
from utils import require_login

# --- PAGE SETUP ---
st.set_page_config(page_title="Admin Panel", layout="wide")
require_login('admin') # Protect this page, only for admins

st.title("👑 Admin Panel")
st.write(f"Selamat datang, **{st.session_state.user_info['name']}**!")

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.header("Menu Admin")
    page = st.radio(
        "Pilih Halaman",
        ["Dashboard", "Manajemen Master MI", "Kegiatan & Batch", "Manajemen User", "Laporan"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key not in ['users_db', 'petugas_db', 'verifikator_db', 'admin_db']:
                del st.session_state[key]
        st.switch_page("streamlit_app.py")


# --- PAGE CONTENT ROUTING ---

if page == "Dashboard":
    st.header("Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Aset di Master", len(st.session_state.admin_db['masterAsetData']))
    with col2:
        st.metric("Total Kegiatan", len(st.session_state.petugas_db['kegiatan']))
    with col3:
        st.metric("Total User Aktif", len(st.session_state.users_db) -1) # Exclude admin
    with col4:
        st.metric("Aset Belum Diverifikasi", len(st.session_state.verifikator_db['verificationList']))

elif page == "Manajemen Master MI":
    st.header("Manajemen Master MI")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        st.button("➕ Tambah Aset", use_container_width=True)
        st.button("⬆️ Import Data", use_container_width=True)

    df = pd.DataFrame(st.session_state.admin_db['masterAsetData'])
    st.dataframe(df, use_container_width=True)

elif page == "Kegiatan & Batch":
    st.header("Kegiatan & Batch")

    # --- Section for Kegiatan ---
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Kegiatan Inventarisasi PHE 2025")
            st.caption("Periode: 01 Jan 2025 - 31 Des 2025")
        with col2:
            if st.button("📝 Buat Kegiatan Baru", use_container_width=True):
                st.info("Fitur ini sedang dalam pengembangan.")

    # --- Section for Batch ---
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Daftar Batch")
        with col2:
            if st.button("➕ Buat Batch Baru", use_container_width=True, type="primary"):
                st.session_state.show_batch_modal = True
        
        # Mock data for display
        batch_data = [
            {"Nama Batch": "Batch 1: Gudang A & B", "Periode": "01 Jul - 31 Jul", "Jumlah Tim": 2, "Verifikator": "Citra Lestari", "Status": "Selesai"},
            {"Nama Batch": "Batch 2: Area Limbah", "Periode": "01 Agu - 31 Agu", "Jumlah Tim": 1, "Verifikator": "Citra Lestari, Budi S.", "Status": "Berlangsung"},
        ]
        st.dataframe(pd.DataFrame(batch_data), use_container_width=True, hide_index=True)


    # --- Modal for Creating a New Batch ---
    if st.session_state.get("show_batch_modal", False):
        @st.dialog("Buat Batch Baru & Atur Tim")
        def create_batch_modal():
            with st.form("new_batch_form"):
                st.text_input("Nama Batch", placeholder="Contoh: Batch 3: Area Terbuka")
                st.markdown("---")
                st.subheader("Tim Pelaksana")

                # Team management logic
                if 'teams' not in st.session_state:
                    st.session_state.teams = []

                if st.button("➕ Tambah Tim"):
                    st.session_state.teams.append({'id': len(st.session_state.teams) + 1})
                    st.rerun() # Rerun to show the new team form

                if not st.session_state.teams:
                    st.info("Belum ada tim yang ditambahkan. Klik 'Tambah Tim' untuk memulai.")

                for i, team in enumerate(st.session_state.teams):
                    with st.container(border=True):
                        st.write(f"**Tim {team['id']}**")
                        
                        # Get users by role
                        petugas_users = {u['name']: email for email, u in st.session_state.users_db.items() if 'petugas' in u.get('assigned_roles', [])}
                        verifikator_users = {u['name']: email for email, u in st.session_state.users_db.items() if 'verifikator' in u.get('assigned_roles', [])}

                        st.multiselect(f"Anggota Tim (Petugas)", options=petugas_users.keys(), key=f"team_members_{i}")
                        st.selectbox(f"Verifikator Tim", options=["-- Pilih Verifikator --"] + list(verifikator_users.keys()), key=f"team_verifier_{i}")

                        if st.button(f"❌ Hapus Tim {team['id']}", key=f"delete_team_{i}"):
                            st.session_state.teams.pop(i)
                            st.rerun()
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                if col1.form_submit_button("Simpan Batch", use_container_width=True, type="primary"):
                    # Logic to save the batch data would go here
                    st.success("Data batch dan tim berhasil disimpan!")
                    st.session_state.show_batch_modal = False
                    del st.session_state.teams # Clean up
                    st.rerun()
                
                if col2.form_submit_button("Batal", use_container_width=True):
                    st.session_state.show_batch_modal = False
                    del st.session_state.teams # Clean up
                    st.rerun()
        
        create_batch_modal()


elif page == "Manajemen User":
    st.header("Manajemen User")
    users_list = []
    for email, user in st.session_state.users_db.items():
        user_data = {
            "Nama": user['name'],
            "Email": email,
            "Tipe Akun": "Admin" if user['role'] == 'admin' else "User",
            "Peran": ", ".join(user.get('assigned_roles', ['-'])),
            "Status": "Aktif" # Mock status
        }
        users_list.append(user_data)
    
    st.dataframe(pd.DataFrame(users_list), use_container_width=True, hide_index=True)


elif page == "Laporan":
    st.header("Laporan Global")
    st.write("Rekapitulasi hasil inventarisasi dari semua batch yang telah selesai.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Selisih Nilai", "Rp 15.250.000", delta="1.2%")
    col2.metric("Aset Baru Ditemukan", "12", delta="5")
    col3.metric("Aset Tidak Ditemukan", "5", delta="-2", delta_color="inverse")

    st.subheader("Pilih Laporan Rinci")
    st.button("Laporan per Lokasi", use_container_width=True)
    st.button("Laporan per Kondisi", use_container_width=True)
    st.button("Laporan Aset Berlebih", use_container_width=True)
