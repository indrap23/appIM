import streamlit as st
import pandas as pd
from utils import require_login
from datetime import datetime

# --- PAGE SETUP ---
st.set_page_config(page_title="Dashboard Verifikator", layout="wide")
require_login('verifikator') # Protect this page

# --- INITIALIZE VIEW STATE ---
if 'verifikator_view' not in st.session_state:
    st.session_state.verifikator_view = 'dashboard'
if 'current_item_id' not in st.session_state:
    st.session_state.current_item_id = None

# --- HELPER FUNCTIONS ---
def get_item_by_id(item_id):
    """Finds a verification item by its ID."""
    for item in st.session_state.verifikator_db['verificationList']:
        if item['id'] == item_id:
            return item
    return None

def change_view(view_name, item_id=None):
    """Function to switch between different screens/views."""
    st.session_state.verifikator_view = view_name
    st.session_state.current_item_id = item_id

# --- HEADER & LOGOUT ---
header_cols = st.columns([3, 1])
with header_cols[0]:
    st.title("✅ Dashboard Verifikator")
    st.write(f"Selamat datang, **{st.session_state.user_info['name']}**!")
with header_cols[1]:
    if st.button("Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key not in ['users_db', 'petugas_db', 'verifikator_db', 'admin_db']:
                del st.session_state[key]
        st.switch_page("streamlit_app.py")
st.markdown("---")

# --- VIEW ROUTING ---

# 1. Dashboard View: Shows list of items to verify
if st.session_state.verifikator_view == 'dashboard':
    st.header("Daftar Aset untuk Diverifikasi")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Menunggu Verifikasi", len(st.session_state.verifikator_db['verificationList']))
    col2.metric("Diverifikasi Hari Ini", "25") # Mock data
    col3.metric("Ditolak Hari Ini", "2") # Mock data
    st.markdown("---")

    verification_list = st.session_state.verifikator_db['verificationList']
    if not verification_list:
        st.info("Tidak ada aset yang menunggu verifikasi saat ini.")
    else:
        df = pd.DataFrame(verification_list)
        # Create a button column for the action
        df['Aksi'] = [f"Periksa_{i}" for i in df['id']]
        
        # Display data using st.dataframe and configure the button column
        st.dataframe(
            df[['desc', 'submittedBy', 'date', 'batch', 'status', 'Aksi']],
            column_config={
                "Aksi": st.column_config.ButtonColumn(
                    "Aksi",
                    help="Klik untuk memeriksa detail aset",
                    width="small"
                )
            },
            on_select="rerun", # Rerun when a row is selected
            hide_index=True,
            use_container_width=True
        )
        
        # Handle button clicks from the dataframe
        if st.session_state.get('selection'):
            selected_rows = st.session_state.selection['rows']
            if selected_rows:
                selected_item_index = selected_rows[0]
                item_id = verification_list[selected_item_index]['id']
                change_view('detail', item_id=item_id)
                st.rerun()


# 2. Detail View: Shows full details for a single item
elif st.session_state.verifikator_view == 'detail':
    item = get_item_by_id(st.session_state.current_item_id)

    if not item:
        st.error("Item tidak ditemukan.")
        if st.button("Kembali ke Daftar"):
            change_view('dashboard')
            st.rerun()
    else:
        if st.button("⬅️ Kembali ke Daftar"):
            change_view('dashboard')
            st.rerun()
        
        st.header(f"Detail Verifikasi: {item['desc']}")
        st.caption(f"ID Verifikasi: {item['id']} | Diinput oleh: {item['submittedBy']} pada {item['date']}")
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Data Baru (Hasil Inventarisasi)")
            with st.container(border=True):
                details = item['details']
                st.write(f"**Klasifikasi:** {details.get('klasifikasi', '-')}")
                st.write(f"**Kondisi:** {details.get('kondisi', '-')}")
                st.write(f"**Kuantitas:** {details.get('kuantitas', '-')} {details.get('satuan', '')}")
                st.write(f"**Lokasi Baru:** {details.get('lokasi', '-')}")
                st.write(f"**Tonase:** {details.get('tonase', '-')} kg")
                st.write(f"**Keterangan:** {details.get('keterangan', '-')}")

            st.subheader("Data Lama (Master)")
            with st.container(border=True):
                if item['previousData']:
                    prev = item['previousData']
                    st.write(f"**Qty Total di Master:** {prev.get('qtyTotal', 'N/A')}")
                    st.write("**Lokasi di Master:**")
                    for loc, qty in prev.get('lokasi', {}).items():
                        st.write(f"- {loc}: **{qty}**")
                else:
                    st.info("Aset ini merupakan temuan baru (tidak ada di data master).")

        with col2:
            st.subheader("Foto Aset")
            for photo in item['photos']:
                st.image(photo, use_column_width=True)

        st.markdown("---")
        st.subheader("Tindakan Verifikasi")
        
        with st.form("verification_action_form"):
            reason = st.text_area("Alasan Penolakan (wajib diisi jika menolak)")
            
            submit_cols = st.columns(2)
            approve_pressed = submit_cols[0].form_submit_button("✅ Setujui", use_container_width=True, type="primary")
            reject_pressed = submit_cols[1].form_submit_button("❌ Tolak (Penelitian Ulang)", use_container_width=True)

            if approve_pressed:
                # In a real app, update the database
                st.session_state.verifikator_db['verificationList'] = [i for i in st.session_state.verifikator_db['verificationList'] if i['id'] != item['id']]
                st.success(f"Aset '{item['desc']}' telah disetujui.")
                change_view('dashboard')
                st.rerun()

            if reject_pressed:
                if not reason:
                    st.error("Mohon isi alasan penolakan.")
                else:
                    # In a real app, update the database with the rejection reason
                    st.session_state.verifikator_db['verificationList'] = [i for i in st.session_state.verifikator_db['verificationList'] if i['id'] != item['id']]
                    st.warning(f"Aset '{item['desc']}' telah ditolak dan dikembalikan untuk penelitian ulang.")
                    change_view('dashboard')
                    st.rerun()
