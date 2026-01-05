import streamlit as st
from groq import Groq
import time

# --- 1. SETUP HALAMAN ---
st.set_page_config(page_title="Asisten Dakwah AI Pro", page_icon="🕌", layout="wide")

# --- 2. CSS & STYLE (Premium Look) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Merriweather:wght@300;400;700&family=Poppins:wght@400;600&display=swap');
    
    .stApp { background-color: #F0F4F8; color: #102A43; }
    
    /* Header */
    h1 { font-family: 'Poppins', sans-serif; color: #004D40 !important; text-align: center; font-weight: 800; font-size: 2.8rem; margin-top: 10px; text-shadow: 1px 1px 0px #fff; }
    .subtitle { font-family: 'Poppins', sans-serif; font-size: 1.1rem; text-align: center; margin-bottom: 30px; color: #546E7A; }
    
    /* Input Container */
    .input-box {
        background-color: white; padding: 30px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #CFD8DC;
    }
    
    /* Progress Bar Custom */
    .stProgress > div > div > div > div { background-color: #009688; }

    /* PAPER RESULT (Kertas Naskah Pro) */
    .kertas-naskah {
        background-color: #FFFFFF; 
        padding: 70px; 
        border-radius: 2px;
        border: 1px solid #E0E0E0;
        font-family: 'Merriweather', serif; /* Font Novel */
        font-size: 1.15rem; 
        line-height: 2.1; 
        color: #263238;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
        margin-top: 30px;
        white-space: pre-wrap;
    }
    
    /* Styles untuk Teks Arab & Elemen Naskah */
    .arab-text { 
        font-family: 'Amiri', serif; 
        font-size: 2.1rem; 
        direction: rtl; 
        color: #1B5E20; 
        line-height: 2.8; 
        margin: 25px 0; 
        display: block; 
        text-align: right;
        border-right: 5px solid #2E7D32;
        padding-right: 20px;
        background: linear-gradient(90deg, transparent, #F1F8E9);
    }
    .terjemahan {
        font-family: 'Poppins', sans-serif;
        font-size: 0.95rem;
        color: #546E7A;
        font-style: italic;
        display: block;
        margin-bottom: 25px;
        padding-left: 20px;
        border-left: 3px solid #CFD8DC;
    }
    .subjudul {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.4rem;
        color: #006064;
        margin-top: 50px;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 2px solid #B2DFDB;
        display: inline-block;
    }
    .quote-box {
        background-color: #ECEFF1;
        padding: 20px;
        border-left: 5px solid #607D8B;
        font-style: italic;
        margin: 20px 0;
        color: #455A64;
    }
    
    /* Button */
    .stButton>button {
        background-image: linear-gradient(to right, #00796B, #009688) !important;
        color: white !important; font-size: 1.2rem !important; font-weight: bold !important;
        padding: 15px 40px !important; border-radius: 50px !important; border: none !important;
        box-shadow: 0 10px 20px rgba(0,150,136,0.3) !important; width: 100%; transition: transform 0.2s;
    }
    .stButton>button:active { transform: scale(0.98); }
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER UI ---
st.markdown("<h1>🕌 ASISTEN DAKWAH AI <span style='color:#FF6F00; font-size:1.5rem; vertical-align:top;'>PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Deep-Dive Generator: Riset Tafsir • Kisah Sirah • Solusi Kontekstual</p>", unsafe_allow_html=True)

# --- 4. CONFIG & INPUT ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = st.text_input("🔑 Masukkan API Key Groq:", type="password")

col_input1, col_input2 = st.columns([1, 2])
with col_input1:
    with st.container():
        st.markdown("### ⚙️ Konfigurasi")
        jenis_naskah = st.radio("Format Naskah", ["Khutbah Jumat (Resmi & Lengkap)", "Kajian Tematik (Mendalam)"])
        audience = st.selectbox("Target Jamaah", ["Umum (Masjid Raya)", "Anak Muda (Gen Z)", "Intelektual/Kantoran", "Masyarakat Pedesaan"])
        durasi_baca = st.select_slider("Target Kedalaman Materi", options=["Standar", "Dalam", "Sangat Mendalam (Buku)"], value="Sangat Mendalam (Buku)")

with col_input2:
    with st.container():
        st.markdown("### 📝 Topik Bahasan")
with col_input2:
    with st.container():
        st.markdown("### 📝 Topik Bahasan")
        # PERHATIKAN: Baris di bawah ini harus satu baris panjang, jangan diputus!
        tema = st.text_input("Tema Spesifik", placeholder="Contoh: Meneladani Kesabaran Nabi Ayub dalam Menghadapi Kebangkrutan...", help="Topik yang spesifik menghasilkan naskah yang lebih tajam.")
        st.info("💡 **Tips:** Sistem akan melakukan 3x proses penulisan bertahap untuk memastikan naskah panjang dan tidak terpotong.")
