import streamlit as st
from utils import require_login

# --- PAGE SETUP ---
st.set_page_config(page_title="Dashboard Petugas", layout="centered")
require_login('petugas') # Protect this page

# --- INITIALIZE VIEW STATE ---
if 'petugas_view' not in st.session_state:
    st.session_state.petugas_view = 'dashboard'
if 'current_kk_id' not in st.session_state:
    st.session_state.current_kk_id = None
if 'current_asset_id' not in st.session_state:
    st.session_state.current_asset_id = None

# --- HELPER FUNCTIONS ---
def get_kertas_kerja_by_id(kk_id):
    """Finds a specific 'Kertas Kerja' by its ID."""
    for kegiatan in st.session_state.petugas_db['kegiatan']:
        for kk in kegiatan['kertasKerja']:
            if kk['id'] == kk_id:
                return kk
    return None

def get_asset_from_kk(kk, asset_id):
    """Finds a specific asset within a 'Kertas Kerja'."""
    if kk:
        for asset in kk['assets']:
            if asset['id'] == asset_id:
                return asset
    return None

def change_view(view_name, kk_id=None, asset_id=None):
    """Function to switch between different screens/views."""
    st.session_state.petugas_view = view_name
    st.session_state.current_kk_id = kk_id
    st.session_state.current_asset_id = asset_id

# --- HEADER & LOGOUT ---
header_cols = st.columns([3, 1])
with header_cols[0]:
    st.title("👷‍♂️ Dashboard Petugas")
    st.write(f"Selamat datang, **{st.session_state.user_info['name']}**!")
with header_cols[1]:
    if st.button("Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key not in ['users_db', 'petugas_db', 'verifikator_db', 'admin_db']:
                del st.session_state[key]
        st.switch_page("streamlit_app.py")
st.markdown("---")


# --- VIEW ROUTING ---

# 1. Dashboard View: Shows list of 'Kertas Kerja'
if st.session_state.petugas_view == 'dashboard':
    st.header("Kertas Kerja Anda")
    for kegiatan in st.session_state.petugas_db['kegiatan']:
        with st.container(border=True):
            st.subheader(kegiatan['name'])
            for kk in kegiatan['kertasKerja']:
                status_color = "error" if kk['status'] == 'Perlu Penelitian Ulang' else "warning"
                st.write(f"**{kk['batch']}**")
                st.progress(kk['progres'] / kk['totalAset'], text=f"Progres: {kk['progres']}/{kk['totalAset']} Aset")
                st.caption(f"Status: :{status_color}[{kk['status']}]")
                if st.button("Buka Kertas Kerja", key=f"open_{kk['id']}", use_container_width=True):
                    change_view('worksheet_detail', kk_id=kk['id'])
                    st.rerun()

# 2. Worksheet Detail View: Shows assets in a 'Kertas Kerja'
elif st.session_state.petugas_view == 'worksheet_detail':
    kk = get_kertas_kerja_by_id(st.session_state.current_kk_id)
    if not kk:
        st.error("Kertas Kerja tidak ditemukan.")
        if st.button("Kembali ke Dashboard"):
            change_view('dashboard')
            st.rerun()
    else:
        if st.button("⬅️ Kembali ke Dashboard"):
            change_view('dashboard')
            st.rerun()
        
        st.header(kk['batch'])
        
        cols = st.columns([2,1])
        cols[0].progress(kk['progres'] / kk['totalAset'], text=f"Progres: {kk['progres']}/{kk['totalAset']} Aset")
        if cols[1].button("➕ Aset Temuan Baru", use_container_width=True):
             change_view('input_new_asset', kk_id=kk['id'])
             st.rerun()

        st.text_input("Cari nama aset...", key="asset_search", placeholder="Filter aset di bawah...")
        
        for asset in kk['assets']:
            # Filter logic
            if st.session_state.asset_search.lower() not in asset['desc'].lower():
                continue

            with st.container(border=True):
                status = asset['status']
                if status == 'Selesai':
                    st.markdown(f"**{asset['desc']}**\n\n*Lokasi: {asset['location']}*")
                    st.success("Selesai ✓")
                else:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{asset['desc']}**\n\n*Lokasi: {asset['location']}*")
                        if 'catatan' in asset:
                            st.error(f"Catatan: {asset['catatan']}")
                    with col2:
                        if st.button("Update Data", key=f"update_{asset['id']}", use_container_width=True):
                            change_view('update_asset', kk_id=kk['id'], asset_id=asset['id'])
                            st.rerun()
        
        st.markdown("---")
        if st.button("Ajukan Verifikasi", use_container_width=True, type="primary"):
            st.success("Aset yang telah diupdate berhasil diajukan untuk verifikasi.")
            change_view('dashboard')
            # In a real app, you would update the status of these assets.

# 3. Update Asset View
elif st.session_state.petugas_view == 'update_asset':
    kk = get_kertas_kerja_by_id(st.session_state.current_kk_id)
    asset = get_asset_from_kk(kk, st.session_state.current_asset_id)

    if not asset:
        st.error("Aset tidak ditemukan.")
        if st.button("Kembali"):
            change_view('worksheet_detail', kk_id=st.session_state.current_kk_id)
            st.rerun()
    else:
        if st.button(f"⬅️ Kembali ke {kk['batch']}"):
            change_view('worksheet_detail', kk_id=kk['id'])
            st.rerun()
        
        st.header(f"Update Aset: {asset['desc']}")
        with st.form("update_asset_form"):
            st.file_uploader("Ambil Foto Aset", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
            c1, c2 = st.columns(2)
            c1.number_input("Kuantitas", min_value=0, value=1)
            c2.text_input("Satuan", value="EA")
            st.selectbox("Kondisi", ["Baik", "Rusak Ringan", "Rusak Berat"])
            st.text_input("Lokasi", value=asset['location'])
            st.text_area("Keterangan", placeholder="Masukkan catatan tambahan...")

            if st.form_submit_button("Simpan Perubahan", use_container_width=True, type="primary"):
                st.success("Data aset berhasil diupdate.")
                # In a real app, you'd save this data and update the asset's status.
                asset['status'] = 'Selesai' # Mock update
                kk['progres'] += 1 # Mock update
                change_view('worksheet_detail', kk_id=kk['id'])
                st.rerun()

# 4. Input New Asset View
elif st.session_state.petugas_view == 'input_new_asset':
    kk = get_kertas_kerja_by_id(st.session_state.current_kk_id)
    if st.button(f"⬅️ Kembali ke {kk['batch']}"):
        change_view('worksheet_detail', kk_id=kk['id'])
        st.rerun()

    st.header("Input Aset Temuan Baru")
    with st.form("new_asset_form"):
        st.text_input("Nama/Deskripsi Aset")
        st.file_uploader("Ambil Foto Aset", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        c1, c2 = st.columns(2)
        c1.number_input("Kuantitas", min_value=1, value=1)
        c2.text_input("Satuan", placeholder="EA")
        st.selectbox("Kondisi", ["Baik", "Rusak Ringan", "Rusak Berat"])
        st.text_input("Lokasi", placeholder="Gudang A / AN-FL-01/C")
        st.text_area("Keterangan", placeholder="Masukkan catatan tambahan...")

        if st.form_submit_button("Simpan Aset Baru", use_container_width=True, type="primary"):
            st.success("Aset temuan baru berhasil disimpan dan diajukan untuk verifikasi.")
            # In a real app, you'd add this new asset to the list.
            change_view('worksheet_detail', kk_id=kk['id'])
            st.rerun()
