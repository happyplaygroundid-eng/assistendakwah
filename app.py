import streamlit as st
from groq import Groq

# --- 1. SETUP HALAMAN ---
st.set_page_config(page_title="Asisten Dakwah AI", page_icon="🕌", layout="centered")

# --- 2. CSS & STYLE (Hijau & Emas) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Poppins:wght@300;400;600;700&display=swap');
    .stApp { background-color: #F1F8E9; color: #1B5E20; }
    h1 { font-family: 'Poppins', sans-serif; color: #1B5E20 !important; text-align: center; font-weight: 700; font-size: 2.5rem; margin-top: 10px; }
    .subtitle { font-family: 'Poppins', sans-serif; font-size: 1rem; text-align: center; margin-bottom: 30px; color: #558B2F; }
    .stButton>button {
        font-family: 'Poppins', sans-serif !important; font-weight: 600 !important;
        background-image: linear-gradient(to right, #2E7D32, #43A047) !important;
        color: white !important; border-radius: 25px !important; border: none !important;
        padding: 12px 25px !important; box-shadow: 0px 4px 10px rgba(46, 125, 50, 0.3) !important; width: 100%;
    }
    .kertas-naskah {
        background-color: #FFFFFF; padding: 40px; border-radius: 15px;
        border-left: 6px solid #F9A825; font-family: 'Poppins', sans-serif; font-size: 1.05rem; line-height: 1.8; color: #212121;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.05); margin-top: 20px; white-space: pre-wrap;
    }
    .arab-text { 
        font-family: 'Amiri', serif; font-size: 1.8rem; direction: rtl; 
        color: #1B5E20; line-height: 2.2; margin: 20px 0; display: block; text-align: right;
        background-color: #F9FBE7; padding: 15px 20px; border-radius: 10px; border-right: 4px solid #33691E;
    }
    .disclaimer-box {
        background-color: #FFF3E0; border: 1px solid #FFE0B2; border-radius: 8px;
        padding: 15px; font-size: 0.85rem; color: #E65100; display: flex; align-items: center; gap: 10px; margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. UI HEADER ---
st.markdown("<h1>🕌 ASISTEN DAKWAH AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Generator Naskah Khutbah Mendalam & Profesional</p>", unsafe_allow_html=True)

# --- 4. API KEY ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = st.text_input("Masukkan API Key Groq Anda:", type="password")

# --- 5. INPUT FORM ---
with st.container(border=True): 
    tema = st.text_input("📝 Tema Dakwah / Topik", placeholder="Contoh: Mengobati Hati yang Gelisah dengan Dzikir...")
    col1, col2 = st.columns(2)
    with col1:
        target_audience = st.selectbox("👥 Target Pendengar", 
            ["Umum / Jamaah Masjid", "Anak Muda / Gen Z (Bahasa Santai)", "Profesional / Kantor", "Majelis Taklim Ibu-ibu"], index=0)
    with col2:
        format_output = st.selectbox("📄 Jenis Materi", 
            ["Naskah Khutbah Jumat (Sangat Lengkap)", "Kultum Mendalam (7-10 Menit)", "Kajian Tematik (20 Menit)"], index=0)

# --- 6. LOGIKA GENERATE (DENGAN TEKNIK CHAIN OF DENSITY) ---
if st.button("✨ BUAT NASKAH MENDALAM ✨"):
    if not api_key or not tema:
        st.warning("⚠️ Mohon lengkapi data terlebih dahulu.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner('⏳ Sedang membuka kitab tafsir & menyusun narasi mendalam... (Mohon sabar, proses ini butuh waktu)'):
                
                # MENENTUKAN STRUKTUR BERDASARKAN JENIS
                if "Khutbah Jumat" in format_output:
                    struktur_instruksi = """
                    ANDA WAJIB MENGIKUTI 5 TAHAP PENULISAN INI SECARA BERURUTAN & PANJANG:
                    
                    BAGIAN 1: KHUTBAH PERTAMA (Minimal 800 Kata)
                    - Mulai dengan Mukadimah Bahasa Arab Lengkap (Hamdalah, Syahadat, Sholawat, Ayat Taqwa).
                    - Sapa jamaah dengan hangat.
                    - Masuk ke pendahuluan masalah yang relate dengan kehidupan saat ini.
                    - Jelaskan definisi topik secara Lughawi (Bahasa) dan Istilah.
                    
                    BAGIAN 2: DALIL & TAFSIR (Minimal 600 Kata)
                    - Kutip 1 Ayat Al-Quran Utama. Tulis Arab, Arti, dan Jelaskan Tafsirnya (Ibnu Katsir/Jalalain) secara mendalam.
                    - Kutip 1 Hadits Shahih. Tulis Arab, Arti, dan bedah makna per-katanya.
                    
                    BAGIAN 3: KISAH RASULULLAH/SAHABAT (Minimal 600 Kata - WAJIB ADA)
                    - Ceritakan SATU kisah spesifik (Sirah Nabawiyah) yang relevan dengan topik secara SANGAT DETAIL.
                    - Gambarkan dialognya, suasananya, dan emosinya. Jangan cuma ringkasan.
                    - Tarik ibrah (pelajaran) dari kisah tersebut.
                    
                    BAGIAN 4: IMPLEMENTASI ZAMAN NOW (Minimal 500 Kata)
                    - Berikan contoh nyata penerapan topik ini di kantor, rumah tangga, atau medsos.
                    - Berikan solusi praktis step-by-step.
                    
                    BAGIAN 5: PENUTUP KHUTBAH 1 & KHUTBAH 2
                    - Kesimpulan Khutbah 1.
                    - Tulis tanda [DUDUK ANTARA DUA KHUTBAH].
                    - Khutbah Kedua (Mukadimah Arab Singkat + Doa Penutup Lengkap Bahasa Arab & Indonesia yang menyentuh hati).
                    """
                else: # Kultum/Kajian
                    struktur_instruksi = """
                    ANDA WAJIB MENGIKUTI STRUKTUR MENDALAM INI:
                    1. PEMBUKAAN (Hook yang kuat, masalah sehari-hari).
                    2. PEMBAHASAN DALIL (Ayat & Hadits wajib Arab+Arti, jelaskan tafsirnya jangan cuma terjemahan).
                    3. STORYTELLING (Kisah Nabi/Salafus Shalih yang diceritakan ulang dengan gaya bercerita/novel, bukan gaya buku sejarah kaku).
                    4. ACTION PLAN (Apa yang harus dilakukan pendengar besok pagi?).
                    5. DOA PENUTUP.
                    (Total Panjang Naskah Wajib Minimal 1.500 Kata).
                    """

                # SYSTEM PROMPT (OTAK USTADZ SENIOR)
                prompt_system = """
                Anda adalah Ustadz Senior dan Cendekiawan Muslim yang sangat dihormati. Gaya bicara Anda tenang, berwibawa, namun sangat menyentuh hati (seperti Buya Hamka atau Ustadz Adi Hidayat).
                
                PANTANGAN KERAS (JANGAN DILAKUKAN):
                ❌ DILARANG MERANGKUM atau menulis "Singkatnya...".
                ❌ DILARANG menggunakan poin-poin (bullet points) yang terlalu banyak. Ubah menjadi narasi paragraf yang mengalir.
                ❌ DILARANG memberikan ceramah yang dangkal/kulitnya saja.
                
                KEWAJIBAN:
                ✅ Gunakan tag <div class='arab-text'>...</div> untuk semua teks Arab.
                ✅ Setiap argumen harus ada sandaran dalilnya.
                ✅ Tulislah selayaknya TRANSKRIP PIDATO ASLI, bukan artikel blog. Gunakan kata seru, pertanyaan retoris, dan sapaan.
                """
                
                prompt_user = f"""
                Topik: {tema}
                Target: {target_audience}
                Jenis: {format_output}
                
                INSTRUKSI KHUSUS:
                {struktur_instruksi}
                
                Mulai menulis sekarang. Pastikan panjang, mendalam, dan menggugah emosi.
                """
                
                # Menggunakan max_tokens tertinggi agar tidak terpotong
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": prompt_system}, 
                        {"role": "user", "content": prompt_user}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=8000, 
                )
                
                st.session_state.naskah_dakwah = chat_completion.choices[0].message.content
                st.session_state.naskah_ready = True
                
        except Exception as e:
            st.error(f"Terjadi Kesalahan: {e}")

# --- 7. HASIL ---
if "naskah_ready" in st.session_state and st.session_state.naskah_ready:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='disclaimer-box'>
        <span style='font-size: 1.5rem;'>⚠️</span>
        <div><strong>Penting:</strong> Naskah ini sangat panjang & mendalam. Mohon dibaca dan dipelajari dulu sebelum naik mimbar.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<div class='kertas-naskah'>{st.session_state.naskah_dakwah}</div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🔄 Buat Baru"):
        st.session_state.naskah_ready = False
        st.rerun()
