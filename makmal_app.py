import streamlit as st
from supabase import create_client, Client
import datetime
import pandas as pd
from datetime import datetime as dt, timedelta
import io
import base64
import time

# ============================================
# KONFIGURASI
# ============================================

SUPABASE_URL = "https://voxsfhphiaxdcxcjxfcw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZveHNmaHBoaWF4ZGN4Y2p4ZmN3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY3MTU2NTMsImV4cCI6MjEwMjI5MTY1M30.7RIWZCp2fiOxwBNIf_Y7pi9tcBHqlZHzmMt7f6ZqVTQ"

# ============================================
# PASSWORD GURU & ADMIN
# ============================================

PASSWORD_GURU = {
    "ehsan": "ehsan123",
    "zul": "zul123",
    "amirah": "amirah123",
    "nada": "nada123",
    "ijat": "ijat123",
    "mas": "mas123",
    "admin": "EHSANfauzi@0"
}

# ============================================
# SAMBUNGAN DATABASE
# ============================================

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# FUNGSI INIT DATABASE
# ============================================

def init_database():
    try:
        supabase.table("tempahan").select("kelas").limit(1).execute()
    except:
        try:
            supabase.rpc('exec_sql', {'sql': 'ALTER TABLE tempahan ADD COLUMN kelas TEXT;'}).execute()
        except:
            pass
        try:
            supabase.rpc('exec_sql', {'sql': 'ALTER TABLE tempahan ADD COLUMN telah_hadir BOOL DEFAULT FALSE;'}).execute()
        except:
            pass

init_database()

# ============================================
# SENARAI GURU & KELAS
# ============================================

GURU = ["ehsan", "zul", "amirah", "nada", "ijat", "mas", "admin"]

TAHUN = ["Tahun 1", "Tahun 2", "Tahun 3", "Tahun 4", "Tahun 5", "Tahun 6"]
KELAS = ["Arif", "Bijak", "Cemerlang"]

JADUAL_WAKTU = {
    "ehsan": {
        "Isnin": "Tahun 1 Arif",
        "Selasa": "Tahun 1 Bijak",
        "Rabu": "Tahun 1 Cemerlang",
        "Khamis": "Tahun 2 Arif",
        "Ahad": "Tahun 2 Bijak"
    },
    "zul": {
        "Isnin": "Tahun 2 Cemerlang",
        "Selasa": "Tahun 3 Arif",
        "Rabu": "Tahun 3 Bijak",
        "Khamis": "Tahun 3 Cemerlang",
        "Ahad": "Tahun 4 Arif"
    },
    "amirah": {
        "Isnin": "Tahun 4 Bijak",
        "Selasa": "Tahun 4 Cemerlang",
        "Rabu": "Tahun 5 Arif",
        "Khamis": "Tahun 5 Bijak",
        "Ahad": "Tahun 5 Cemerlang"
    },
    "nada": {
        "Isnin": "Tahun 6 Arif",
        "Selasa": "Tahun 6 Bijak",
        "Rabu": "Tahun 6 Cemerlang",
        "Khamis": "Tahun 1 Arif",
        "Ahad": "Tahun 1 Bijak"
    },
    "ijat": {
        "Isnin": "Tahun 1 Cemerlang",
        "Selasa": "Tahun 2 Arif",
        "Rabu": "Tahun 2 Bijak",
        "Khamis": "Tahun 2 Cemerlang",
        "Ahad": "Tahun 3 Arif"
    },
    "mas": {
        "Isnin": "Tahun 3 Bijak",
        "Selasa": "Tahun 3 Cemerlang",
        "Rabu": "Tahun 4 Arif",
        "Khamis": "Tahun 4 Bijak",
        "Ahad": "Tahun 4 Cemerlang"
    }
}

SLOT_MASA = [
    ("7:45", "8:15"),
    ("8:15", "8:45"),
    ("8:45", "9:15"),
    ("9:15", "9:45"),
    ("9:45", "10:15"),
    ("10:15", "10:45"),
    ("10:45", "11:15"),
    ("11:15", "11:45"),
    ("11:45", "12:15"),
    ("12:15", "12:45"),
    ("12:45", "13:15"),
]

HARI_BEKERJA = [0, 1, 2, 3, 6]

# ============================================
# FUNGSI TEMPAHAN
# ============================================

def dapatkan_tempahan(tarikh):
    response = supabase.table("tempahan")\
        .select("*")\
        .eq("tarikh", str(tarikh))\
        .eq("status", "aktif")\
        .execute()
    return response.data

def buat_tempahan(tarikh, slot_mula, slot_tamat, guru, kelas, aktiviti, no_telefon):
    data = {
        "tarikh": str(tarikh),
        "slot_mula": slot_mula,
        "slot_tamat": slot_tamat,
        "guru": guru,
        "kelas": kelas,
        "aktiviti": aktiviti,
        "no_telefon": no_telefon,
        "status": "aktif",
        "telah_hadir": False
    }
    result = supabase.table("tempahan").insert(data).execute()
    return result

def batal_tempahan(tempahan_id):
    response = supabase.table("tempahan").select("*").eq("id", tempahan_id).execute()
    if response.data:
        tempahan = response.data[0]
        supabase.table("tempahan")\
            .update({"status": "batal"})\
            .eq("id", tempahan_id)\
            .execute()
        return True
    return False

def tandakan_hadir(tempahan_id):
    supabase.table("tempahan")\
        .update({"telah_hadir": True})\
        .eq("id", tempahan_id)\
        .execute()

# ============================================
# FUNGSI POP-UP
# ============================================

def popup_success(mesej):
    sound_html = """
    <audio autoplay>
        <source src="https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3" type="audio/mpeg">
    </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)
    st.balloons()
    st.success(mesej)
    time.sleep(0.5)

def popup_error(mesej):
    st.error(mesej)

def popup_warning(mesej):
    st.warning(mesej)

def popup_info(mesej):
    st.info(mesej)

# ============================================
# FUNGSI EXPORT
# ============================================

def export_excel(data, title):
    if not data:
        return None
    
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Laporan', index=False)
    return output.getvalue()

def export_pdf(data, title):
    if not data:
        return None
    
    df = pd.DataFrame(data)
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h1 {{ color: #0a2463; text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background-color: #0a2463; color: white; padding: 10px; text-align: left; }}
            td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
            tr:hover {{ background-color: #f5f5f5; }}
        </style>
    </head>
    <body>
        <h1>🧪 {title}</h1>
        <p>Dijana pada: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}</p>
        {df.to_html(index=False)}
    </body>
    </html>
    """
    return html

# ============================================
# DASHBOARD GURU
# ============================================

def dashboard_guru(guru_name):
    st.subheader(f"📊 Dashboard {guru_name}")
    
    response = supabase.table("tempahan")\
        .select("*")\
        .eq("guru", guru_name)\
        .eq("status", "aktif")\
        .execute()
    
    data = response.data
    
    if not data:
        st.info(f"📌 Tiada tempahan untuk {guru_name}.")
        return
    
    df = pd.DataFrame(data)
    df['tarikh'] = pd.to_datetime(df['tarikh'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Jumlah Tempahan", len(df))
    with col2:
        bulan_ini = datetime.date.today().month
        tempahan_bulan_ini = len(df[df['tarikh'].dt.month == bulan_ini])
        st.metric("📅 Bulan Ini", tempahan_bulan_ini)
    with col3:
        if not df.empty:
            kelas_teratas = df['kelas'].mode()[0]
            st.metric("📚 Kelas Paling Kerap", kelas_teratas)
        else:
            st.metric("📚 Kelas Paling Kerap", "-")
    
    st.subheader("📋 Senarai Tempahan Anda")
    df_display = df[['tarikh', 'kelas', 'slot_mula', 'slot_tamat', 'aktiviti']]
    df_display.columns = ['Tarikh', 'Kelas', 'Slot Mula', 'Slot Tamat', 'Aktiviti']
    st.dataframe(df_display, use_container_width=True)

# ============================================
# SESSION STATE INIT
# ============================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_guru = None
if 'slot_terpilih' not in st.session_state:
    st.session_state.slot_terpilih = []
if 'previous_tempoh' not in st.session_state:
    st.session_state.previous_tempoh = "30 Minit (1 slot)"
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ============================================
# LOGIN SYSTEM
# ============================================

def login():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Login")
    
    if not st.session_state.logged_in:
        nama = st.sidebar.selectbox("Pilih Nama Guru", GURU)
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login", use_container_width=True):
            if PASSWORD_GURU.get(nama) == password:
                st.session_state.logged_in = True
                st.session_state.current_guru = nama
                st.sidebar.success(f"✅ Login berjaya! {nama}")
                st.rerun()
            else:
                st.sidebar.error("❌ Password salah!")
    else:
        st.sidebar.success(f"👋 Logged in as: **{st.session_state.current_guru}**")
        if st.sidebar.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_guru = None
            st.session_state.slot_terpilih = []
            st.rerun()

# ============================================
# DARK MODE TOGGLE
# ============================================

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# ============================================
# STREAMLIT UI
# ============================================

st.set_page_config(
    page_title="🧪 Sistem Tempahan Makmal Sains",
    page_icon="🧪",
    layout="wide"
)

# ============================================
# LOGIN PAGE
# ============================================

if not st.session_state.logged_in:
    st.markdown("""
    <style>
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 80vh;
            background: linear-gradient(135deg, #0a2463 0%, #1e3a5f 30%, #5c2d91 70%, #2ecc71 100%);
            border-radius: 20px;
            padding: 2rem;
            margin: -2rem;
        }
        .login-box {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 3rem 4rem;
            border-radius: 2rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
            width: 100%;
            border: 2px solid rgba(255,255,255,0.2);
        }
        .login-title {
            font-size: 3.5rem;
            font-weight: 800;
            color: #0a2463;
            margin-bottom: 0.2rem;
            font-family: 'Orbitron', sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .login-subtitle {
            font-size: 1.2rem;
            color: #5c2d91;
            margin-bottom: 1.5rem;
        }
        .login-icon {
            font-size: 4rem;
            margin-bottom: 0.5rem;
        }
        .login-divider {
            border: none;
            height: 3px;
            background: linear-gradient(to right, #0a2463, #5c2d91, #2ecc71);
            margin: 1.5rem 0;
            border-radius: 10px;
        }
        .login-footer {
            margin-top: 1.5rem;
            color: #6c757d;
            font-size: 0.85rem;
        }
        .login-footer strong {
            color: #0a2463;
        }
        .login-badge {
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            color: white;
            padding: 0.3rem 1.2rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-top: 0.5rem;
        }
        @media (max-width: 600px) {
            .login-box {
                padding: 2rem 1.5rem;
            }
            .login-title {
                font-size: 2.5rem;
            }
            .login-container {
                padding: 1rem;
                min-height: 70vh;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="login-container">
        <div class="login-box">
            <div class="login-icon">🧪</div>
            <div class="login-title">MAKMAL SAINS</div>
            <div style="font-size: 1.5rem; color: #0a2463; font-weight: 600;">🔬</div>
            <div class="login-subtitle">
                Sistem Tempahan Makmal Sains<br>
                <span style="font-size: 0.9rem; color: #6c757d;">Sekolah Kebangsaan</span>
            </div>
            <div class="login-badge">⚡ Mudah & Cepat</div>
            <hr class="login-divider">
            <div style="font-size: 1.1rem; color: #1e3a5f; font-weight: 500; margin-bottom: 0.5rem;">
                👋 Selamat Datang!
            </div>
            <div style="font-size: 0.95rem; color: #555; margin-bottom: 1rem;">
                Sila login menggunakan akaun anda di sebelah kiri 👈
            </div>
            <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
                <div style="background: #e8f4f8; padding: 0.5rem 1rem; border-radius: 10px; font-size: 0.8rem;">
                    👨‍🏫 Guru
                </div>
                <div style="background: #f0e6ff; padding: 0.5rem 1rem; border-radius: 10px; font-size: 0.8rem;">
                    👑 Admin
                </div>
                <div style="background: #d4edda; padding: 0.5rem 1rem; border-radius: 10px; font-size: 0.8rem;">
                    📚 Kelas
                </div>
            </div>
            <div class="login-footer">
                <strong>🧪 Makmal Sains Sekolah</strong> &bull; v6.0<br>
                <span style="font-size: 0.75rem; color: #aaa;">© 2026 | Dibangunkan untuk guru-guru sains</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    login()
    st.stop()

# ============================================
# CSS
# ============================================

st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #0a2463;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-title {
        text-align: center;
        color: #5c2d91;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .slot-selected {
        background: linear-gradient(135deg, #0a2463, #5c2d91) !important;
        color: white !important;
        padding: 0.7rem;
        border-radius: 0.8rem;
        text-align: center;
        border: 3px solid #2ecc71 !important;
        margin: 0.2rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .slot-booked {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb) !important;
        padding: 0.7rem;
        border-radius: 0.8rem;
        text-align: center;
        border: 2px solid #dc3545 !important;
        margin: 0.2rem 0;
    }
    .slot-booked small {
        display: block;
        font-size: 0.7rem;
        color: #721c24;
        margin-top: 0.2rem;
    }
    .dashboard-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid #2ecc71;
    }
    .footer {
        text-align: center;
        color: #6c757d;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #ddd;
    }
    @media (max-width: 600px) {
        .stColumns {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 0.5rem !important;
        }
        .stColumns > div {
            width: 100% !important;
            min-width: 0 !important;
        }
        .main-title {
            font-size: 1.8rem !important;
        }
        .sub-title {
            font-size: 0.9rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

if st.session_state.dark_mode:
    st.markdown("""
    <style>
        .stApp { background: #0f172a !important; }
        .stSidebar { background: #1e293b !important; }
        .main-title { color: #ffffff !important; }
        .sub-title { color: #a78bfa !important; }
        p, h1, h2, h3, h4, label, .stMarkdown { color: #f1f5f9 !important; }
        .stSelectbox label, .stDateInput label, .stTextInput label, .stTextArea label { color: #f1f5f9 !important; }
        .stRadio label { color: #f1f5f9 !important; }
        .dashboard-card { 
            background: #1e293b !important; 
            color: #f1f5f9 !important; 
            border-left: 5px solid #818cf8 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        }
        .dashboard-card h4 { color: #ffffff !important; }
        .footer { color: #94a3b8 !important; border-top-color: #334155 !important; }
        .stDataFrame { background: #1e293b !important; color: #f1f5f9 !important; }
        .stDataFrame thead th { background: #0f172a !important; color: #ffffff !important; }
        .stDataFrame tbody td { color: #f1f5f9 !important; border-bottom: 1px solid #334155 !important; }
        .stAlert { background: #1e293b !important; color: #f1f5f9 !important; border: 1px solid #475569 !important; }
        .stAlert p { color: #f1f5f9 !important; }
        .stTextInput input, .stTextArea textarea, .stSelectbox select, .stDateInput input {
            background: #1e293b !important;
            color: #f1f5f9 !important;
            border: 1px solid #475569 !important;
        }
        .stButton button {
            background: #3b82f6 !important;
            color: white !important;
            border: 1px solid #60a5fa !important;
        }
        .stButton button:hover { background: #2563eb !important; }
        [data-testid="metric-container"] {
            background: #1e293b !important;
            padding: 1rem !important;
            border-radius: 0.5rem !important;
            border: 1px solid #334155 !important;
        }
        [data-testid="metric-container"] p { color: #f1f5f9 !important; }
        [data-testid="metric-container"] h1 { color: #a78bfa !important; }
        .slot-selected {
            background: linear-gradient(135deg, #1e40af, #5b21b6) !important;
            color: #ffffff !important;
            border: 3px solid #34d399 !important;
        }
        .slot-booked {
            background: linear-gradient(135deg, #7f1d1d, #991b1b) !important;
            color: #fca5a5 !important;
            border: 2px solid #ef4444 !important;
        }
        .slot-booked small { color: #fca5a5 !important; }
        .stSidebar p, .stSidebar label, .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4 {
            color: #f1f5f9 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# MAIN APP
# ============================================

login()

if not st.session_state.logged_in:
    st.stop()

with st.sidebar:
    st.markdown("---")
    tema = "🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"
    if st.button(tema, use_container_width=True):
        toggle_dark_mode()

st.markdown('<h1 class="main-title">🧪 Sistem Tempahan Makmal Sains</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">🔬 Makmal Sains Sekolah | 📚 Tempah & Urus Penggunaan Makmal</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    menu = st.radio(
        "📋 Navigasi",
        ["📅 Tempah Makmal", "📊 Jadual Makmal", "📈 Dashboard Admin", "👤 Dashboard Saya", "❌ Batal Tempahan", "📚 Jadual Waktu Guru"]
    )
    st.markdown("---")
    st.caption("🧪 v6.0 | Dibangunkan untuk guru-guru sains")

# ============================================
# MENU 1: TEMPAH MAKMAL
# ============================================

if menu == "📅 Tempah Makmal":
    st.subheader("📅 Buat Tempahan Baru")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        tarikh = st.date_input(
            "Pilih Tarikh",
            datetime.date.today(),
            min_value=datetime.date.today(),
            max_value=datetime.date.today() + timedelta(days=30)
        )
        
        hari_tinggal = (tarikh - datetime.date.today()).days
        if hari_tinggal == 0:
            popup_info("📌 Tempahan untuk HARI INI! 🏃‍♂️")
        elif hari_tinggal == 1:
            popup_warning("⏰ Tempahan untuk ESOK! Jangan lupa!")
        elif hari_tinggal <= 3:
            popup_info(f"📅 Tempahan dalam {hari_tinggal} hari lagi")
        else:
            popup_info(f"📅 Tempahan dalam {hari_tinggal} hari lagi")
        
        if tarikh.weekday() not in HARI_BEKERJA:
            popup_error("⚠️ Maaf, sekolah hanya buka Ahad - Khamis. Sila pilih tarikh lain.")
            st.stop()
        
        guru = st.selectbox("Pilih Guru", GURU, index=GURU.index(st.session_state.current_guru))
        
        tahun = st.selectbox("Pilih Tahun", TAHUN)
        kelas = st.selectbox("Pilih Kelas", KELAS)
        kelas_full = f"{tahun} {kelas}"
        
        no_telefon = st.text_input("No. Telefon", "0137203123")
        aktiviti = st.text_area("Aktiviti / Eksperimen", placeholder="Contoh: Eksperimen Kitaran Air")
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h4>📌 Panduan</h4>
            <ul>
                <li>Pilih tarikh</li>
                <li>Pilih guru & kelas</li>
                <li>Klik slot hijau</li>
                <li>Pilih tempoh</li>
                <li>Klik Tempah</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("🕐 Pilih Slot Masa")
    
    tempahan_sedia = dapatkan_tempahan(tarikh)
    slot_ditempah = {}
    for t in tempahan_sedia:
        for i in range(t['slot_mula'], t['slot_tamat'] + 1):
            slot_ditempah[i] = {
                'guru': t['guru'],
                'kelas': t['kelas'],
                'aktiviti': t['aktiviti']
            }
    
    tempoh = st.radio("Tempoh", ["30 Minit (1 slot)", "60 Minit (2 slot berturut-turut)"])
    
    if st.session_state.previous_tempoh != tempoh:
        st.session_state.slot_terpilih = []
        st.session_state.previous_tempoh = tempoh
    
    cols = st.columns(4)
    
    for i, (mula, tamat) in enumerate(SLOT_MASA):
        with cols[i % 4]:
            is_booked = i in slot_ditempah
            is_selected = i in st.session_state.slot_terpilih
            
            if is_booked:
                info = slot_ditempah[i]
                st.markdown(f"""
                <div class="slot-booked">
                    ❌ {mula}-{tamat}<br>
                    <small>👨‍🏫 {info['guru']}</small>
                    <small>📚 {info['kelas']}</small>
                    <small>🔬 {info['aktiviti'][:20]}...</small>
                </div>
                """, unsafe_allow_html=True)
            elif is_selected:
                st.markdown(f"""
                <div class="slot-selected">
                    🔵 {mula}-{tamat}<br>
                    <small>✅ Dipilih</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"✅ {mula}-{tamat}", key=f"slot_{i}", use_container_width=True):
                    if tempoh == "60 Minit (2 slot berturut-turut)":
                        if len(st.session_state.slot_terpilih) == 0:
                            st.session_state.slot_terpilih.append(i)
                            popup_success(f"✅ Slot {mula}-{tamat} dipilih! Pilih slot bersebelahan.")
                        elif len(st.session_state.slot_terpilih) == 1:
                            last_slot = st.session_state.slot_terpilih[0]
                            if abs(i - last_slot) == 1:
                                st.session_state.slot_terpilih.append(i)
                                popup_success(f"✅ {SLOT_MASA[last_slot][0]}-{SLOT_MASA[last_slot][1]} + {mula}-{tamat} dipilih! (60 Minit)")
                            else:
                                st.session_state.slot_terpilih = [i]
                                popup_warning(f"🔄 Tukar ke slot {mula}-{tamat}. Pilih slot bersebelahan.")
                        else:
                            popup_warning("⚠️ Anda sudah pilih 2 slot.")
                    else:
                        if len(st.session_state.slot_terpilih) == 0:
                            st.session_state.slot_terpilih.append(i)
                            popup_success(f"✅ Slot {mula}-{tamat} dipilih! (30 Minit)")
                        else:
                            st.session_state.slot_terpilih = [i]
                            popup_warning(f"🔄 Tukar ke slot {mula}-{tamat} (30 Minit)")
    
    if st.session_state.slot_terpilih:
        selected_slots = sorted(st.session_state.slot_terpilih)
        slot_text = " + ".join([f"{SLOT_MASA[i][0]}-{SLOT_MASA[i][1]}" for i in selected_slots])
        popup_info(f"📌 Slot dipilih: {slot_text}")
        
        if st.button("🔄 Batal Pilihan", type="secondary", use_container_width=True):
            st.session_state.slot_terpilih = []
            popup_info("✅ Pilihan dibatalkan.")
    
    if st.button("📝 Tempah Sekarang", type="primary", use_container_width=True):
        if not st.session_state.slot_terpilih:
            popup_warning("⚠️ Sila pilih slot masa yang kosong.")
        else:
            sorted_slots = sorted(st.session_state.slot_terpilih)
            slot_mula = sorted_slots[0]
            slot_tamat = sorted_slots[-1]
            
            if tempoh == "60 Minit (2 slot berturut-turut)":
                if len(sorted_slots) != 2:
                    popup_error("❌ Untuk 60 minit, sila pilih 2 slot.")
                elif slot_tamat != slot_mula + 1:
                    popup_error("❌ Untuk 60 minit, 2 slot mesti berturut-turut.")
                else:
                    buat_tempahan(tarikh, slot_mula, slot_tamat, guru, kelas_full, aktiviti, no_telefon)
                    popup_success("✅ Tempahan 60 Minit BERJAYA! 🎉")
                    st.session_state.slot_terpilih = []
                    st.rerun()
            else:
                if len(sorted_slots) != 1:
                    popup_error("❌ Untuk 30 minit, sila pilih 1 slot sahaja.")
                else:
                    buat_tempahan(tarikh, slot_mula, slot_mula, guru, kelas_full, aktiviti, no_telefon)
                    popup_success("✅ Tempahan 30 Minit BERJAYA! 🎉")
                    st.session_state.slot_terpilih = []
                    st.rerun()

# ============================================
# MENU 2: JADUAL MAKMAL
# ============================================

elif menu == "📊 Jadual Makmal":
    st.subheader("📊 Jadual Makmal")
    
    tarikh_lihat = st.date_input("Pilih Tarikh", datetime.date.today())
    
    hari_tinggal = (tarikh_lihat - datetime.date.today()).days
    if hari_tinggal == 0:
        popup_info("📌 Jadual untuk HARI INI")
    elif hari_tinggal == 1:
        popup_warning("📌 Jadual untuk ESOK")
    elif hari_tinggal > 1:
        popup_info(f"📌 Jadual untuk {hari_tinggal} hari lagi")
    
    if tarikh_lihat.weekday() not in HARI_BEKERJA:
        popup_warning("📌 Sekolah cuti pada hari ini.")
    else:
        tempahan = dapatkan_tempahan(tarikh_lihat)
        if not tempahan:
            popup_info("📌 Tiada tempahan pada hari ini.")
        else:
            df = pd.DataFrame(tempahan)
            df['Masa'] = df.apply(lambda x: f"{SLOT_MASA[x['slot_mula']][0]} - {SLOT_MASA[x['slot_tamat']][1]}", axis=1)
            df_display = df[['guru', 'Masa', 'kelas', 'aktiviti', 'no_telefon']]
            df_display.columns = ['Guru', 'Masa', 'Kelas', 'Aktiviti', 'No. Telefon']
            st.dataframe(df_display, use_container_width=True)

# ============================================
# MENU 3: DASHBOARD ADMIN
# ============================================

elif menu == "📈 Dashboard Admin":
    st.subheader("📈 Dashboard Admin")
    
    if st.session_state.current_guru != "admin":
        popup_error("⛔ Akses ditolak! Halaman ini hanya untuk admin.")
        st.stop()
    
    tarikh_mula = st.date_input("Dari", datetime.date.today() - timedelta(days=30))
    tarikh_akhir = st.date_input("Hingga", datetime.date.today())
    
    response = supabase.table("tempahan")\
        .select("*")\
        .gte("tarikh", str(tarikh_mula))\
        .lte("tarikh", str(tarikh_akhir))\
        .execute()
    
    data = response.data
    
    if not data:
        popup_info("📌 Tiada tempahan dalam tempoh ini.")
    else:
        df = pd.DataFrame(data)
        df['tarikh'] = pd.to_datetime(df['tarikh'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 Jumlah Tempahan", len(df))
        with col2:
            st.metric("👨‍🏫 Guru Paling Aktif", df['guru'].mode()[0] if not df.empty else "-")
        with col3:
            hari_ini = datetime.date.today()
            tempahan_hari_ini = len(df[df['tarikh'].dt.date == hari_ini])
            st.metric("📅 Tempahan Hari Ini", tempahan_hari_ini)
        with col4:
            hadir = len(df[df.get('telah_hadir', False) == True])
            st.metric("✅ Telah Hadir", hadir)
        
        st.subheader("📊 Statistik Mengikut Guru")
        st.bar_chart(df['guru'].value_counts())
        
        st.subheader("📊 Statistik Mengikut Bulan")
        df['bulan'] = df['tarikh'].dt.strftime('%B %Y')
        st.bar_chart(df['bulan'].value_counts())
        
        st.subheader("📋 Senarai Tempahan")
        df_display = df[['tarikh', 'guru', 'kelas', 'slot_mula', 'slot_tamat', 'aktiviti', 'status']]
        df_display.columns = ['Tarikh', 'Guru', 'Kelas', 'Slot Mula', 'Slot Tamat', 'Aktiviti', 'Status']
        st.dataframe(df_display, use_container_width=True)
        
        st.subheader("✅ Tandakan Telah Hadir")
        tempahan_aktif = df[df['status'] == 'aktif']
        if not tempahan_aktif.empty:
            for idx, row in tempahan_aktif.iterrows():
                if not row.get('telah_hadir', False):
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                    with col1:
                        st.write(row['guru'])
                    with col2:
                        st.write(row['kelas'])
                    with col3:
                        st.write(row['tarikh'].strftime('%d/%m/%Y'))
                    with col4:
                        st.write(f"{SLOT_MASA[row['slot_mula']][0]} - {SLOT_MASA[row['slot_tamat']][1]}")
                    with col5:
                        if st.button("✅ Hadir", key=f"hadir_{row['id']}"):
                            tandakan_hadir(row['id'])
                            popup_success("✅ Tandakan hadir berjaya!")
                            st.rerun()
        else:
            popup_info("📌 Tiada tempahan aktif yang perlu ditanda hadir.")
        
        st.subheader("🔍 Carian Tempahan")
        cari = st.text_input("Cari (Nama Guru / Tarikh)")
        if cari:
            hasil = df[df['guru'].str.contains(cari, case=False) | 
                      df['tarikh'].astype(str).str.contains(cari)]
            if not hasil.empty:
                st.dataframe(hasil[['tarikh', 'guru', 'kelas', 'aktiviti']])
            else:
                popup_info("📌 Tiada hasil carian.")
        
        st.subheader("📥 Export Laporan")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Export PDF", use_container_width=True):
                html = export_pdf(data, "Laporan Tempahan Makmal Sains")
                if html:
                    b64 = base64.b64encode(html.encode()).decode()
                    href = f'<a href="data:text/html;base64,{b64}" download="laporan_tempahan.html">📥 Klik untuk muat turun PDF (HTML)</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    popup_success("✅ PDF siap! Klik link di atas untuk muat turun.")
        with col2:
            if st.button("📊 Export Excel", use_container_width=True):
                try:
                    excel_data = export_excel(data, "Laporan Tempahan Makmal Sains")
                    if excel_data:
                        b64 = base64.b64encode(excel_data).decode()
                        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="laporan_tempahan.xlsx">📥 Klik untuk muat turun Excel</a>'
                        st.markdown(href, unsafe_allow_html=True)
                        popup_success("✅ Excel siap! Klik link di atas untuk muat turun.")
                except Exception as e:
                    popup_error(f"❌ Error: {e}. Pastikan 'xlsxwriter' sudah install.")

# ============================================
# MENU 4: DASHBOARD GURU
# ============================================

elif menu == "👤 Dashboard Saya":
    if st.session_state.current_guru == "admin":
        popup_warning("👋 Admin, anda tidak mempunyai data tempahan peribadi. Sila gunakan Dashboard Admin.")
    else:
        dashboard_guru(st.session_state.current_guru)

# ============================================
# MENU 5: BATAL TEMPAHAN
# ============================================

elif menu == "❌ Batal Tempahan":
    st.subheader("❌ Batal Tempahan")
    
    if st.session_state.current_guru == "admin":
        popup_warning("👋 Admin, anda tidak boleh membatalkan tempahan. Ini untuk guru-guru sahaja.")
    else:
        tarikh_batal = st.date_input("Pilih Tarikh", datetime.date.today())
        tempahan = dapatkan_tempahan(tarikh_batal)
        
        tempahan_guru = [t for t in tempahan if t['guru'] == st.session_state.current_guru]
        
        if not tempahan_guru:
            popup_info(f"📌 Tiada tempahan aktif untuk {st.session_state.current_guru} pada tarikh ini.")
        else:
            for t in tempahan_guru:
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                with col1:
                    st.write(f"👨‍🏫 {t['guru']}")
                with col2:
                    st.write(f"📚 {t['kelas']}")
                with col3:
                    st.write(f"🕐 {SLOT_MASA[t['slot_mula']][0]} - {SLOT_MASA[t['slot_tamat']][1]}")
                with col4:
                    st.write(f"🔬 {t['aktiviti']}")
                with col5:
                    if st.button("❌ Batal", key=f"batal_{t['id']}"):
                        if batal_tempahan(t['id']):
                            popup_success("✅ Tempahan dibatalkan!")
                            st.rerun()
                st.divider()

# ============================================
# MENU 6: JADUAL WAKTU GURU
# ============================================

elif menu == "📚 Jadual Waktu Guru":
    st.subheader("📚 Jadual Waktu Guru Sains")
    
    guru_pilih = st.selectbox("Pilih Guru", GURU)
    
    if guru_pilih:
        jadual = JADUAL_WAKTU[guru_pilih]
        
        data_jadual = []
        for hari, kelas in jadual.items():
            data_jadual.append({"Hari": hari, "Kelas": kelas})
        
        df_jadual = pd.DataFrame(data_jadual)
        st.dataframe(df_jadual, use_container_width=True)
        
        st.subheader("📋 Jadual Semua Guru")
        semua_data = []
        for guru, jadual in JADUAL_WAKTU.items():
            for hari, kelas in jadual.items():
                semua_data.append({"Guru": guru, "Hari": hari, "Kelas": kelas})
        
        df_semua = pd.DataFrame(semua_data)
        st.dataframe(df_semua, use_container_width=True)

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    🧪 Sistem Tempahan Makmal Sains v6.0 | Dibangunkan untuk guru-guru sains<br>
    <small>© 2026 | 🔬 Makmal Sains Sekolah</small>
</div>
""", unsafe_allow_html=True)
