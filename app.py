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
    
    /* PAPER RESULT (Kertas Naskah Pro) */
    .kertas-naskah {
        background-color: #FFFFFF; 
        padding: 70px; 
        border-radius: 2px;
        border: 1px solid #E0E0E0;
        font-family: 'Merriweather', serif; 
        font-size: 1.15rem; 
        line-height: 2.1; 
        color: #263238;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
        margin-top: 30px;
        white-space: pre-wrap;
    }
    
    /* Styles untuk Teks Arab */
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
    .subjudul {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.4rem;
        color: #006064;
        margin-top: 50px;
        margin-bottom: 20px;
        text-transform: uppercase;
        border-bottom: 2px solid #B2DFDB;
        display: inline-block;
    }
    
    /* Button */
    .stButton>button {
        background-image: linear-gradient(to right, #00796B, #009688) !important;
        color: white !important; font-size: 1.2rem !important; font-weight: bold !important;
        padding: 15px 40px !important; border-radius: 50px !important; border: none !important;
        box-shadow: 0 10px 20px rgba(0,150,136,0.3) !important; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER UI ---
st.markdown("<h1>🕌 ASISTEN DAKWAH AI <span style='color:#FF6F00; font-size:1.5rem; vertical-align:top;'>PRO</span></h1>", unsafe_allow_html=True)

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
        audience = st.selectbox("Target Jamaah", ["Umum (Masjid Raya)", "Anak Muda (Gen Z)", "Intelektual/Kantoran"])

with col_input2:
    with st.container():
        st.markdown("### 📝 Topik Bahasan")
        tema = st.text_input("Tema Spesifik", placeholder="Contoh: Meneladani Kesabaran Nabi Ayub...", help="Topik yang spesifik menghasilkan naskah yang lebih tajam.")
        st.info("💡 **Tips:** Sistem akan melakukan 3x proses penulisan bertahap untuk memastikan naskah panjang.")

# --- 5. LOGIKA GENERATOR BERTAHAP (CHAINING) ---
if st.button("🚀 MULAI PENYUSUNAN NASKAH (DEEP MODE)"):
    if not api_key or not tema:
        st.error("⚠️ Mohon lengkapi API Key dan Tema.")
    else:
        client = Groq(api_key=api_key)
        full_naskah = ""
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # === TAHAP 1: PEMBUKAAN & TAFSIR ===
            status_text.markdown("#### 🔄 Tahap 1/3: Membedah Tafsir & Dalil...")
            progress_bar.progress(10)
            
            prompt_1 = f"""
            Anda adalah Ulama Ahli Tafsir. Tulis BAGIAN PEMBUKA & LANDASAN DALIL untuk '{tema}'.
            INSTRUKSI:
            1. Judul & Mukadimah Arab Lengkap (Gunakan <div class='arab-text'>...</div>).
            2. Pendahuluan masalah.
            3. BEDAH DALIL: Kutip 1 Ayat Utama (Arab & Arti) & Jelaskan Tafsir Lughawi (Makna kata per kata).
            """
            response_1 = client.chat.completions.create(
                messages=[{"role": "system", "content": "Anda Ahli Tafsir."}, {"role": "user", "content": prompt_1}],
                model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=3000
            )
            full_naskah += response_1.choices[0].message.content + "\n\n"
            
            # === TAHAP 2: STORYTELLING ===
            status_text.markdown("#### 🔄 Tahap 2/3: Menulis Kisah Sirah & Solusi...")
            progress_bar.progress(50)
            
            prompt_2 = f"""
            Anda Pencerita Ulung. Lanjutkan naskah.
            INSTRUKSI:
            1. Subjudul: <div class='subjudul'>KISAH TELADAN</div>
            2. Ceritakan 1 Kisah Sirah Nabi/Sahabat secara DETAIL (Dialog & Emosi). Jangan merangkum!
            3. Subjudul: <div class='subjudul'>KONTEKSTUALISASI</div>
            4. Sambungkan kisah dengan masalah zaman now & berikan 3 Solusi Praktis.
            """
            response_2 = client.chat.completions.create(
                messages=[{"role": "system", "content": "Anda Pencerita."}, {"role": "user", "content": prompt_2}],
                model="llama-3.3-70b-versatile", temperature=0.8, max_tokens=4000
            )
            full_naskah += response_2.choices[0].message.content + "\n\n"

            # === TAHAP 3: PENUTUP ===
            status_text.markdown("#### 🔄 Tahap 3/3: Menyusun Doa Mustajab...")
            progress_bar.progress(80)
            
            prompt_3 = f"""
            Anda Imam Besar. Tulis PENUTUP untuk naskah ini.
            INSTRUKSI:
            1. Kesimpulan.
            2. [Jika Khutbah Jumat] Tulis tanda Duduk Antara Dua Khutbah & Khutbah Kedua Singkat.
            3. DOA PENUTUP LENGKAP (Arab & Arti) yang menyentuh hati.
            """
            response_3 = client.chat.completions.create(
                messages=[{"role": "system", "content": "Anda Imam."}, {"role": "user", "content": prompt_3}],
                model="llama-3.3-70b-versatile", temperature=0.6, max_tokens=2000
            )
            full_naskah += response_3.choices[0].message.content
            
            # === SELESAI ===
            progress_bar.progress(100)
            st.session_state.final_naskah = full_naskah
            st.session_state.naskah_done = True
            st.rerun() # <--- INI SOLUSINYA

        except Exception as e:
            st.error(f"Error: {e}")

# --- 6. DISPLAY HASIL ---
if "naskah_done" in st.session_state and st.session_state.naskah_done:
    st.markdown("---")
    st.success("✅ Naskah Selesai!")
    st.markdown(f"<div class='kertas-naskah'>{st.session_state.final_naskah}</div>", unsafe_allow_html=True)
    if st.button("🔄 Buat Baru"):
        st.session_state.naskah_done = False
        st.rerun()
