import streamlit as st

# This file centralizes data and helper functions to keep other scripts clean.

def get_initial_data():
    """
    Returns all the initial hardcoded data from the original JS application.
    This makes it easy to manage and modify the demo data in one place.
    """
    return {
        'users': {
            'admin@lman.go.id': {'role': 'admin', 'name': 'Admin LMAN'},
            'user@lman.go.id': {'role': 'user', 'name': 'Budi Santoso', 'assigned_roles': ['petugas', 'verifikator']},
            'ani@lman.go.id': {'role': 'user', 'name': 'Ani Wijaya', 'assigned_roles': ['petugas']},
            'citra@lman.go.id': {'role': 'user', 'name': 'Citra Lestari', 'assigned_roles': ['verifikator']},
            'dodi@lman.go.id': {'role': 'user', 'name': 'Dodi Firmansyah', 'assigned_roles': ['petugas']}
        },
        'petugas_data': {
            'kegiatan': [
                {
                    'id': 'KEG-PHE-2025',
                    'name': 'Inventarisasi Aset Proyek PHE 2025',
                    'kertasKerja': [
                        { 'id': 'KK-001', 'batch': 'Inv. Limbah - Agustus 2025', 'totalAset': 150, 'progres': 2, 'status': 'Berlangsung',
                          'assets': [
                              { 'id': 'LBH-0451', 'desc': 'BEAM - 250 MM X 125 MM', 'location': 'Area Limbah', 'status': 'Selesai' },
                              { 'id': 'LBH-0452', 'desc': 'PIPA - BESI 6 INCH', 'location': 'Area Limbah', 'status': 'Selesai' },
                              { 'id': 'LBH-0453', 'desc': 'DRUM - BEKAS OLI', 'location': 'Area Limbah', 'status': 'Belum Diperiksa' },
                          ]},
                        { 'id': 'KK-002', 'batch': 'Inv. Gudang A - Juli 2025', 'totalAset': 1, 'progres': 0, 'status': 'Perlu Penelitian Ulang',
                          'assets': [
                              { 'id': 'VLV-1001', 'desc': 'VALVE BUTTERFLY, 16IN', 'location': 'Gudang A', 'status': 'Perlu Diperiksa Ulang', 'catatan': 'Foto tidak jelas.' }
                          ]}
                    ]
                }
            ],
        },
        'verifikator_data': {
            'verificationList': [
                { 'id': 'LMAN-VLV-1001', 'materialCode': '5200036051', 'desc': 'VALVE BUTTERFLY, 16IN, 150LB', 'submittedBy': 'Budi Santoso', 'date': '25/07/2025 10:30', 'batch': 'Inv. Gudang A - Juli 2025', 'kegiatan': 'Inventarisasi Aset Proyek PHE 2025', 'status': 'Menunggu Verifikasi', 'photos': ['https://placehold.co/600x400/cccccc/666666?text=Foto+Valve+1', 'https://placehold.co/600x400/cccccc/666666?text=Foto+Valve+2'], 'details': { 'klasifikasi': 'Metal', 'kondisi': 'Baik', 'kuantitas': '1', 'satuan': 'EA', 'tonase': '50', 'dimensi': '40x40x30 cm', 'expiredDate': '2030-12-31', 'assetGroup': '2. Piping System', 'keterangan': 'Ditemukan di rak bagian atas.', 'lokasi': 'Gudang A / AN-FL-01/C' }, 'previousData': { 'qtyTotal': 2, 'lokasi': {'AN-FL-01/C': 1, 'AN-FL-02/A': 1} } },
                { 'id': 'LMAN-LBH-0451', 'materialCode': '5200036817', 'desc': 'BEAM - 250 MM X 125 MM X 6', 'submittedBy': 'Ani Wijaya', 'date': '25/07/2025 09:10', 'batch': 'Inv. Limbah - Agustus 2025', 'kegiatan': 'Inventarisasi Aset Proyek PHE 2025', 'status': 'Menunggu Verifikasi', 'photos': ['https://placehold.co/600x400/cccccc/666666?text=Foto+BEAM'], 'details': { 'klasifikasi': 'Metal', 'kondisi': 'Rusak Berat', 'kuantitas': '1', 'satuan': 'EA', 'tonase': '1200', 'dimensi': '', 'expiredDate': '', 'assetGroup': '', 'keterangan': 'Korosi parah di beberapa bagian.', 'lokasi': 'Area Limbah / Blok C' }, 'previousData': { 'qtyTotal': 1, 'lokasi': {'YD-SHELTER': 1} } },
                { 'id': 'LMAN-NEW-001', 'materialCode': '', 'desc': 'COMPRESSOR ANGIN BEKAS', 'submittedBy': 'Budi Santoso', 'date': '26/07/2025 11:00', 'batch': 'Inv. Gudang A - Juli 2025', 'kegiatan': 'Inventarisasi Aset Proyek PHE 2025', 'status': 'Menunggu Verifikasi', 'photos': ['https://placehold.co/600x400/cccccc/666666?text=Foto+Compressor'], 'details': { 'klasifikasi': 'Metal', 'kondisi': 'Rusak Ringan', 'kuantitas': '1', 'satuan': 'Unit', 'tonase': '250', 'dimensi': '120x80x100 cm', 'expiredDate': '', 'assetGroup': '', 'keterangan': 'Aset temuan baru, tidak ada di master data.', 'lokasi': 'Gudang A / Pojok Belakang' }, 'previousData': None },
            ]
        },
        'admin_data': {
            'masterAsetData': [
                { 'code': '5200007420', 'desc': 'VALVE-SAFETY,TYPE: NS255DB,1.5 IN 300', 'qty': 1, 'unit': 'EA', 'location': 'AN PH-10' },
                { 'code': '5200036051', 'desc': 'VALVE BUTTERFLY, 16IN, 150LB', 'qty': 2, 'unit': 'EA', 'location': 'AN-FL-01/C' },
                { 'code': '5200035623', 'desc': 'VALVE - GATE, 8IN, 150LB, EXTEN.STEM', 'qty': 1, 'unit': 'EA', 'location': 'AN-FL-02/A' },
                { 'code': '5200036817', 'desc': 'BEAM - 250 MM X 125 MM X 6', 'qty': 1, 'unit': 'EA', 'location': 'YD-SHELTER' },
                { 'code': '5200036825', 'desc': 'PLATE - STEEL,1/8IN X 4 X 8 FT, MATL CS', 'qty': 0, 'unit': 'EA', 'location': 'YD-SHELTER' }
            ]
        }
    }

def init_session_state():
    """
    Initializes session_state with data if it's the first run.
    This prevents data from being reset on every interaction.
    """
    if 'initialized' not in st.session_state:
        data = get_initial_data()
        st.session_state.users_db = data['users']
        st.session_state.petugas_db = data['petugas_data']
        st.session_state.verifikator_db = data['verifikator_data']
        st.session_state.admin_db = data['admin_data']
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.session_state.initialized = True


def login_user(email):
    """
    Checks user credentials and updates session_state.
    """
    email = email.strip().lower()
    if email in st.session_state.users_db:
        st.session_state.logged_in = True
        st.session_state.user_info = st.session_state.users_db[email]
        st.session_state.user_info['email'] = email # Add email to user_info
        return True
    return False

def require_login(role_or_roles=None):
    """
    A decorator-like function to protect pages.
    It checks if a user is logged in and has the required role.
    
    Args:
        role_or_roles (str or list, optional): The required role(s). 
                                               Can be 'admin', 'petugas', 'verifikator', or a list.
    """
    if not st.session_state.get("logged_in"):
        st.error("🔒 Anda harus login untuk mengakses halaman ini.")
        st.page_link("streamlit_app.py", label="Kembali ke Halaman Login", icon="🏠")
        st.stop()

    if role_or_roles:
        user_info = st.session_state.user_info
        # Normalize to a list
        required = [role_or_roles] if isinstance(role_or_roles, str) else role_or_roles
        
        # Check admin role directly
        is_admin = user_info.get('role') == 'admin'
        # Check assigned roles for regular users
        user_assigned_roles = user_info.get('assigned_roles', [])

        # The user has access if they are an admin OR have one of the required roles assigned.
        if not (is_admin and 'admin' in required or any(r in user_assigned_roles for r in required)):
            st.error("🚫 Anda tidak memiliki hak akses untuk halaman ini.")
            st.page_link("streamlit_app.py", label="Kembali ke Halaman Utama", icon="🏠")
            st.stop()
