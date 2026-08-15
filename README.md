# 🧪 Sistem Tempahan Makmal Sains

Sistem tempahan makmal sains untuk guru-guru di sekolah. Mudah, cepat, dan mesra pengguna.

---

## ✨ Ciri-ciri Utama

- Tempah 30 minit atau 60 minit
- Pilih kelas (Tahun 1-6 + Arif/Bijak/Cemerlang)
- Dashboard Admin dengan statistik & export PDF/Excel
- Dashboard Guru untuk lihat tempahan sendiri
- Batal tempahan sendiri
- Jadual Waktu Guru
- Dark Mode
- Responsive untuk komputer & telefon

---

## 🔐 Login

| Pengguna | Nama | Password |
|----------|------|----------|
| Guru | `ehsan`, `zul`, `amirah`, `nada`, `ijat`, `mas` | `nama+123` (contoh: `ehsan123`) |
| Admin | `admin` | `EHSANfauzi@0` |

---

## 🛠️ Teknologi

- **Python** + **Streamlit** — App
- **Supabase** — Database
- **Pandas** — Data
- **XlsxWriter** — Export Excel

---

## 🚀 Cara Jalankan

```bash
# Clone repository
git clone https://github.com/sekolah-makmal/makmal-sains.git
cd makmal-sains

# Buat virtual environment
python3 -m venv makmal_env
source makmal_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Jalankan app
streamlit run makmal_app.py
