import streamlit as st
from groq import Groq
import datetime

# --- 1. SETUP HALAMAN (Nuansa Islami Clean) ---
st.set_page_config(page_title="Asisten Dakwah AI", page_icon="🕌", layout="centered")

# --- 2. CSS & STYLE (Hijau & Emas - FIX UI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Background & Text */
    .stApp { background-color: #F1F8E9; color: #1B5E20; }
    
    /* Typography */
    h1 { font-family: 'Poppins', sans-serif; color: #1B5E20 !important; text-align: center; font-weight: 700; font-size: 2.5rem; margin-top: 20px; }
    .subtitle { font-family: 'Poppins', sans-serif; font-size: 1rem; text-align: center; margin-bottom: 20px; color: #558B2F; }
    label { font-family: 'Poppins', sans-serif !important; color: #33691E !important; font-weight: 600 !important; }

    /* Input Container (Card Style) */
    .input-container {
        background-color: white; padding: 25px; border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #DCEDC8;
        margin-bottom: 20px;
    }

    /* Input Fields */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 10px !important; border: 1px solid #C5E1A5 !important;
        background-color: #FAFAFA !important; color: #000000 !important;
    }

    /* Buttons */
    .stButton>button {
        font-family: 'Poppins', sans-serif !important; font-weight: 600 !important;
        background-image: linear-gradient(to right, #2E7D32, #43A047) !important;
        color: white !important; border-radius: 25px !important; border: none !important;
        padding: 12px 25px !important; box-shadow: 0px 4px 10px rgba(46, 125, 50, 0.3) !important;
        width: 100%; transition: all 0.2s;
    }
    .stButton>button:hover { box-shadow: 0px 6px 15px rgba(46, 125, 50, 0.4) !important; transform: translateY(-2px); }
    
    /* Result Box (Kertas Naskah) */
    .kertas-naskah {
        background-color: #FFFFFF; padding: 40px; border-radius: 15px;
        border-left: 6px solid #F9A825; /* Aksen Emas */
        font-family: 'Poppins', sans-serif; font-size: 1.05rem; line-height: 1.8; color: #212121;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.05); margin-top: 20px;
        white-space: pre-wrap; /* Agar paragraf rapi */
    }
    
    /* ARABIC TEXT STYLE (PENTING) */
    .arab-text { 
        font-family: 'Amiri', serif; font-size: 1.6rem; direction: rtl; 
        color: #1B5E20; line-height: 2.2; margin: 15px 0; display: block; text-align: right;
    }
    
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
st.markdown("<p class='subtitle'>Buat Materi Kultum & Khutbah Lengkap dengan Dalil Arab</p>", unsafe_allow_html=True)

# --- 4. API KEY ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = st.text_input("Masukkan API Key Groq Anda:", type="password")

# --- 5. INPUT FORM ---
# Menggunakan container biasa tanpa HTML injection yang berlebihan biar gak ada blok putih aneh
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    tema = st.text_input("📝 Tema Dakwah / Topik", placeholder="Contoh: Sabar Menghadapi Ujian, Keutamaan Sedekah Subuh...")
    
    col1, col2 = st.columns(2)
    with col1:
        target_audience = st.selectbox("👥 Target Pendengar", 
            ["Umum / Jamaah Masjid", "Anak Muda / Gen Z (Bahasa Santai)", "Perkantoran / Profesional", "Ibu-ibu Pengajian"], 
            index=0)
    with col2:
        # Poin-poin ceramah SUDAH DIHAPUS dari sini
        format_output = st.selectbox("📄 Jenis Materi", 
            ["Kultum Singkat (7 Menit)", "Naskah Khutbah Jumat (Lengkap 20 Menit)", "Caption Sosmed (IG/TikTok)"], 
            index=0)
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. LOGIKA GENERATE ---
if st.button("✨ BUAT NASKAH LENGKAP ✨"):
    if not api_key:
        st.error("⚠️ API Key belum dimasukkan!")
    elif not tema:
        st.warning("⚠️ Mohon isi Tema Dakwah terlebih dahulu.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner('⏳ Sedang membuka kitab & menyusun naskah... (Mohon tunggu sebentar)'):
                
                # SETTING PANJANG KATA BERDASARKAN PILIHAN
                min_kata = "800 kata" # Default Kultum
                struktur_khusus = ""
                
                if "Khutbah Jumat" in format_output:
                    min_kata = "1500 sampai 2000 kata (Sangat Panjang)"
                    struktur_khusus = "Wajib Format Khutbah Jumat Resmi (Khutbah Pertama + Khutbah Kedua + Doa Penutup)."
                elif "Caption" in format_output:
                    min_kata = "150-200 kata"
                    struktur_khusus = "Gaya bahasa caption menarik, gunakan bullet points dan hashtag."

                # SYSTEM PROMPT (OTAK USTADZ)
                prompt_system = """
                Anda adalah Ulama/Ustadz cerdas yang ahli menyusun naskah ceramah.
                
                ATURAN FORMAT (WAJIB DIPATUHI):
                1. DALIL: Setiap mengutip Ayat Al-Quran atau Hadits, WAJIB menuliskan:
                   - Teks Arab Asli (Gunakan Font Arabic UTF-8 yang benar).
                   - Terjemahan Bahasa Indonesia.
                   - Sumber (Nama Surat:Ayat atau Perawi Hadits).
                
                2. PANJANG & KEDALAMAN: 
                   - Jangan membuat naskah pendek! Bahas topik secara mendalam, runut, dan tuntas.
                   - Gunakan analogi atau kisah inspiratif agar pendengar tidak bosan.
                
                3. STRUKTUR OUTPUT:
                   - Judul (Kapital & Menarik).
                   - Mukadimah (Salam, Hamdalah, Sholawat - Lengkap Arab & Arti).
                   - Isi Materi (Bagi menjadi beberapa sub-poin yang detail).
                   - Penutup & Doa.
                   - [PENTING] Bagian Terakhir: Buat kotak "RANGKUMAN / POIN PENTING" untuk catatan penceramah.
                """
                
                prompt_user = f"""
                Buatkan Naskah Dakwah.
                Topik: {tema}
                Target Audiens: {target_audience}
                Jenis: {format_output}
                
                Instruksi Khusus:
                - Panjang Naskah: Minimal {min_kata}.
                - {struktur_khusus}
                - Gunakan tag HTML <div class='arab-text'>...teks arab...</div> untuk setiap teks Arab agar tampilannya rapi kanan-kiri.
                """
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": prompt_system}, 
                        {"role": "user", "content": prompt_user}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=6000, # Diperbesar agar naskah tidak terpotong
                )
                
                result_text = chat_completion.choices[0].message.content
                st.session_state.naskah_dakwah = result_text
                st.session_state.naskah_ready = True
                
        except Exception as e:
            st.error(f"Terjadi Kesalahan: {e}")

# --- 7. HASIL ---
if "naskah_ready" in st.session_state and st.session_state.naskah_ready:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # DISCLAIMER
    st.markdown("""
    <div class='disclaimer-box'>
        <span style='font-size: 1.5rem;'>⚠️</span>
        <div>
            <strong>Disclaimer:</strong> Mohon koreksi kembali Teks Arab & Terjemahan sebelum disampaikan.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KOTAK NASKAH
    # Note: unsafe_allow_html=True diaktifkan agar tag <div class='arab-text'> dari AI bisa dirender jadi font Arab yang bagus
    st.markdown(f"<div class='kertas-naskah'>{st.session_state.naskah_dakwah}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🔄 Reset / Buat Baru"):
        st.session_state.naskah_ready = False
        st.rerun()
