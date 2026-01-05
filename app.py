import streamlit as st
from groq import Groq
import datetime

# --- 1. SETUP HALAMAN (Nuansa Islami) ---
st.set_page_config(page_title="Asisten Dakwah AI", page_icon="🕌", layout="centered")

# --- 2. CSS & STYLE (Hijau & Emas) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Poppins:wght@300;400;600&display=swap');
    
    /* Background & Text */
    .stApp { background-color: #F1F8E9; color: #1B5E20; }
    
    /* Typography */
    h1 { font-family: 'Poppins', sans-serif; color: #1B5E20 !important; text-align: center; font-weight: 700; margin-bottom: 0px; }
    .subtitle { font-family: 'Poppins', sans-serif; font-size: 1.1rem; text-align: center; margin-bottom: 30px; color: #558B2F; }
    label { font-family: 'Poppins', sans-serif !important; color: #33691E !important; font-weight: 600 !important; }

    /* Input Fields */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 10px !important; border: 1px solid #C5E1A5 !important;
        background-color: #FFFFFF !important; color: #000000 !important;
    }

    /* Buttons */
    .stButton>button {
        font-family: 'Poppins', sans-serif !important; font-weight: 600 !important;
        background-image: linear-gradient(to right, #2E7D32, #43A047) !important;
        color: white !important; border-radius: 25px !important; border: none !important;
        padding: 12px 25px !important; box-shadow: 0px 4px 10px rgba(46, 125, 50, 0.3) !important;
        width: 100%;
    }
    .stButton>button:hover { box-shadow: 0px 6px 15px rgba(46, 125, 50, 0.4) !important; transform: translateY(-2px); }
    
    /* Result Box (Kertas Naskah) */
    .kertas-naskah {
        background-color: #FFFFFF; padding: 40px; border-radius: 15px;
        border-left: 5px solid #F9A825; /* Aksen Emas */
        font-family: 'Poppins', sans-serif; font-size: 1rem; line-height: 1.8; color: #212121;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    
    /* Arabic Text Style */
    .arab-text { font-family: 'Amiri', serif; font-size: 1.4rem; direction: rtl; color: #1B5E20; }
    
    /* Disclaimer Box */
    .disclaimer-box {
        background-color: #FFF3E0; border: 1px solid #FFE0B2; border-radius: 8px;
        padding: 15px; font-size: 0.85rem; color: #E65100; display: flex; align-items: center; gap: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. JUDUL ---
st.markdown("<h1>🕌 ASISTEN DAKWAH AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Buat Materi Kultum, Khutbah, & Konten Dakwah dalam Sekejap</p>", unsafe_allow_html=True)

# --- 4. API KEY ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = st.text_input("Masukkan API Key Groq Anda:", type="password")

# --- 5. INPUT FORM ---
with st.container():
    st.markdown("<div style='background-color: white; padding: 25px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);'>", unsafe_allow_html=True)
    
    tema = st.text_input("📝 Tema Dakwah / Topik", placeholder="Contoh: Sabar Menghadapi Ujian, Keutamaan Sedekah Subuh...")
    
    col1, col2 = st.columns(2)
    with col1:
        target_audience = st.selectbox("👥 Target Pendengar (Audiens)", 
            ["Umum / Jamaah Masjid", "Anak Muda / Gen Z (Bahasa Santai)", "Anak-anak (Bahasa Sederhana)", "Perkantoran / Profesional"], 
            index=0)
    with col2:
        format_output = st.selectbox("📄 Format Output", 
            ["Kultum Singkat (7 Menit)", "Naskah Khutbah Jumat (Lengkap)", "Caption Instagram/TikTok", "Poin-poin Ceramah"], 
            index=0)
            
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. LOGIKA GENERATE ---
if st.button("✨ BUAT MATERI DAKWAH ✨"):
    if not api_key:
        st.error("⚠️ API Key belum dimasukkan!")
    elif not tema:
        st.warning("⚠️ Mohon isi Tema Dakwah terlebih dahulu.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner('⏳ Sedang menyusun materi & mencari dalil...'):
                
                # SYSTEM PROMPT (OTAK USTADZ)
                prompt_system = """
                Anda adalah seorang Dai/Ustadz yang berilmu, bijak, dan tegas.
                Tugas Anda: Membuat materi dakwah yang menyentuh hati dan berlandaskan Al-Quran & Sunnah.
                
                Aturan Penting:
                1. GAYA BAHASA: Sesuaikan dengan Target Audiens. Jika Gen Z, gunakan pendekatan relate tapi sopan. Jika Umum, gunakan bahasa formal dan wibawa.
                2. DALIL: Wajib menyertakan Ayat Al-Quran atau Hadits yang relevan. Tuliskan Terjemahannya. Pastikan kutipan AKURAT dan YAKIN (Jangan ragu-ragu).
                3. STRUKTUR: Buka dengan salam & hamdalah, Isi Materi (Poin penting), Tutup dengan doa/kesimpulan.
                4. Hindari kata-kata "Saya tidak yakin", "Mungkin", atau "Maaf saya AI". Jadilah asisten yang meyakinkan.
                """
                
                prompt_user = f"Tema: {tema}. Target: {target_audience}. Format: {format_output}. Buatkan materi lengkapnya."
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": prompt_system}, 
                        {"role": "user", "content": prompt_user}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.6,
                    max_tokens=3500, 
                )
                
                result_text = chat_completion.choices[0].message.content
                st.session_state.naskah_dakwah = result_text
                st.session_state.naskah_ready = True
                
        except Exception as e:
            st.error(f"Terjadi Kesalahan: {e}")

# --- 7. HASIL (TANPA AUDIO) ---
if "naskah_ready" in st.session_state and st.session_state.naskah_ready:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # DISCLAIMER TETAP ADA (UI)
    st.markdown("""
    <div class='disclaimer-box'>
        <span style='font-size: 1.5rem;'>⚠️</span>
        <div>
            <strong>Disclaimer AI:</strong> Naskah ini disusun oleh kecerdasan buatan. 
            Mohon cek kembali ketepatan Ayat & Hadits sebelum disampaikan ke publik.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KOTAK NASKAH
    st.markdown(f"<div class='kertas-naskah'>{st.session_state.naskah_dakwah.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🔄 Reset / Buat Baru"):
        st.session_state.naskah_ready = False
        st.rerun()
