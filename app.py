import streamlit as st
from groq import Groq

# --- 1. SETUP HALAMAN ---
st.set_page_config(page_title="Asisten Dakwah AI", page_icon="🕌", layout="wide") # Layout Wide biar lega

# --- 2. CSS & STYLE (Clean & Professional Look) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Merriweather:wght@300;400;700&family=Poppins:wght@400;600&display=swap');
    
    .stApp { background-color: #F4F6F0; color: #212121; }
    
    /* Header Styles */
    h1 { font-family: 'Poppins', sans-serif; color: #1B5E20 !important; text-align: center; font-weight: 700; font-size: 2.5rem; margin-top: 10px; }
    .subtitle { font-family: 'Poppins', sans-serif; font-size: 1.1rem; text-align: center; margin-bottom: 40px; color: #558B2F; }
    
    /* Input Area */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background-color: white; padding: 30px; border-radius: 15px; border: 1px solid #E0E0E0;
    }
    
    /* Tombol */
    .stButton>button {
        font-family: 'Poppins', sans-serif !important; font-weight: 600 !important; font-size: 1.1rem !important;
        background-image: linear-gradient(to right, #2E7D32, #66BB6A) !important;
        color: white !important; border-radius: 10px !important; border: none !important;
        padding: 15px 30px !important; transition: all 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(46,125,50,0.3); }

    /* PAPER STYLE RESULT (Kertas Naskah) */
    .kertas-naskah {
        background-color: #FFFFFF; 
        padding: 60px; 
        border-radius: 2px;
        border: 1px solid #D7D7D7;
        font-family: 'Merriweather', serif; /* Font kayak buku/novel biar enak dibaca */
        font-size: 1.1rem; 
        line-height: 2.0; /* Spasi lega buat baca di mimbar */
        color: #2C2C2C;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); 
        margin-top: 20px;
        white-space: pre-wrap;
    }
    
    /* ARABIC STYLE (Jelas & Besar) */
    .arab-text { 
        font-family: 'Amiri', serif; 
        font-size: 2.0rem; 
        direction: rtl; 
        color: #004D40; 
        line-height: 2.6; 
        margin: 25px 0; 
        display: block; 
        text-align: right;
        font-weight: 400;
        background: linear-gradient(to left, #E0F2F1, transparent); /* Highlight halus */
        padding: 10px 20px;
        border-right: 5px solid #00695C;
    }
    
    /* Terjemahan Dalil */
    .terjemahan {
        font-style: italic;
        color: #546E7A;
        font-size: 0.95rem;
        margin-bottom: 20px;
        display: block;
    }

    /* Sub-Heading dalam Naskah */
    .naskah-subjudul {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.3rem;
        color: #1B5E20;
        margin-top: 40px;
        margin-bottom: 15px;
        text-decoration: underline;
        text-decoration-color: #A5D6A7;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. UI HEADER ---
st.markdown("<h1>🕌 ASISTEN DAKWAH AI (PRO)</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Generator Naskah Khutbah Mendalam • Tafsir • Sirah • Hadits</p>", unsafe_allow_html=True)

# --- 4. API KEY ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = st.text_input("Masukkan API Key Groq Anda:", type="password")

# --- 5. INPUT FORM ---
col_main1, col_main2 = st.columns([1, 2]) # Layout kiri kecil, kanan besar

with col_main1:
    st.markdown("### ⚙️ Pengaturan")
    format_output = st.radio("Jenis Naskah", 
        ["Khutbah Jumat (Lengkap)", "Kultum / Kajian (7-15 Menit)"])
    
    target_audience = st.selectbox("Target Jamaah", 
        ["Umum (Masjid Raya)", "Anak Muda (Bahasa Relate)", "Perkantoran/Intelektual", "Masyarakat Desa"])
    
    gaya_bahasa = st.selectbox("Gaya Penyampaian", 
        ["Tegas & Membakar Semangat (Hamka Style)", "Lembut & Menyentuh Hati (Aa Gym Style)", "Cerdas & Analitis (UAH Style)"])

with col_main2:
    st.markdown("### 📝 Topik Dakwah")
    tema = st.text_input("Judul / Tema Spesifik", placeholder="Misal: Bahaya Riba di Era Pinjol, atau Keajaiban Sholat Tahajud...", help="Semakin spesifik topiknya, semakin bagus hasilnya.")
    
    st.markdown(" ") # Spacer
    if st.button("🚀 SUSUN NASKAH LENGKAP"):
        # LOGIKA GENERATE
        if not api_key or not tema:
            st.error("⚠️ Mohon isi API Key dan Tema terlebih dahulu.")
        else:
            try:
                client = Groq(api_key=api_key)
                with st.spinner('⏳ Sedang membuka kitab tafsir, mencari hadits shahih, dan menyusun narasi... (Mohon tunggu 1-2 menit)'):
                    
                    # --- PROMPT ENGINEERING LEVEL: EXPERT ---
                    
                    # 1. Tentukan Struktur Ketat
                    if "Khutbah Jumat" in format_output:
                        struktur = """
                        WAJIB IKUTI STRUKTUR INI (JANGAN DIUBAH):
                        1. [KHUTBAH PERTAMA] Mukadimah Arab Lengkap (Hamdalah, Syahadat, Sholawat, Wasiat Taqwa).
                        2. [PENDAHULUAN] Hook masalah sosial terkini yang relate dengan jamaah.
                        3. [PEMBAHASAN DALIL] Bedah 1 Ayat Al-Quran (Tafsir Lughawi/Bahasa) & 1 Hadits Shahih. JANGAN CUMA TERJEMAHAN, tapi jelaskan makna per katanya.
                        4. [KISAH TELADAN] Ceritakan Sirah Nabi/Sahabat secara NARATIF (Ada dialog, ada emosi, minimal 400 kata untuk bagian kisah ini saja).
                        5. [KONTEKSTUALISASI] Solusi nyata untuk kehidupan modern.
                        6. [PENUTUP KHUTBAH 1] Kesimpulan singkat khutbah 1.
                        7. [DUDUK DI ANTARA DUA KHUTBAH] Tulis teks: "Duduk sejenak..."
                        8. [KHUTBAH KEDUA] Mukadimah Arab Singkat + Doa Penutup Lengkap (Arab & Indo).
                        """
                    else:
                        struktur = """
                        STRUKTUR KAJIAN:
                        1. Pembukaan Menarik (Storytelling).
                        2. Landasan Dalil (Bedah Ayat & Hadits secara mendalam).
                        3. Kisah Inspiratif (Wajib Sirah Nabawiyah yang detail).
                        4. Action Plan (Apa yang harus dilakukan jamaah).
                        5. Doa Penutup.
                        """

                    # 2. System Prompt "Anti-Summarize"
                    prompt_system = f"""
                    Anda adalah Penulis Naskah Pidato Dakwah Profesional yang setara dengan Ulama Besar ({gaya_bahasa}).
                    
                    PANTANGAN KERAS (DILARANG):
                    ❌ JANGAN gunakan bullet points (1, 2, 3) di dalam isi materi. Tulislah dalam PARAGRAF NARATIF yang mengalir seperti orang bercerita.
                    ❌ JANGAN merangkum kisah. Ceritakan kisah Nabi dengan detail, sertakan dialog dan deskripsi suasana agar jamaah menangis/tersentuh.
                    ❌ JANGAN kaku seperti buku paket. Gunakan sapaan: "Hadirin rahimakumullah", "Saudaraku yang dirahmati Allah".
                    ❌ JANGAN pendek. Anda dibayar mahal untuk naskah yang PANJANG dan MENDALAM.
                    
                    ATURAN TEKNIS:
                    ✅ SETIAP mengutip Arab, GUNAKAN format: <div class='arab-text'>[TEKS ARAB]</div> <span class='terjemahan'>Artinya: [TERJEMAHAN]</span>
                    ✅ Sertakan referensi hadits yang jelas (misal: HR. Bukhari No. 1234).
                    ✅ Gunakan sub-judul dengan format: <div class='naskah-subjudul'>[JUDUL BAGIAN]</div>
                    """
                    
                    prompt_user = f"""
                    Buatkan naskah dakwah LENGKAP.
                    Topik: {tema}
                    Target: {target_audience}
                    
                    Ikuti struktur ini:
                    {struktur}
                    
                    Mulai menulis sekarang. Pastikan panjang, menyentuh hati, dan ilmiah.
                    """
                    
                    # 3. Call API dengan Token Maksimal
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": prompt_system}, 
                            {"role": "user", "content": prompt_user}
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.75, # Sedikit lebih kreatif biar gak kaku
                        max_tokens=8000, 
                    )
                    
                    st.session_state.naskah_dakwah = chat_completion.choices[0].message.content
                    st.session_state.naskah_ready = True
            
            except Exception as e:
                st.error(f"Terjadi Kesalahan: {e}")

# --- 6. HASIL (Full Width Paper) ---
if "naskah_ready" in st.session_state and st.session_state.naskah_ready:
    st.markdown("---")
    st.success("✅ Naskah berhasil disusun! Silakan copy atau baca langsung di bawah ini.")
    
    # Render HTML langsung agar CSS Arab & Style berfungsi maksimal
    st.markdown(f"<div class='kertas-naskah'>{st.session_state.naskah_dakwah}</div>", unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns([1,4])
    with col_btn1:
        if st.button("🗑️ Hapus & Buat Baru"):
            st.session_state.naskah_ready = False
            st.rerun()
