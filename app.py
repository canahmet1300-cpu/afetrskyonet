import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
import folium
from streamlit_folium import st_folium

# --- 1. AYARLAR VE DÜZELTİLMİŞ TASARIM ---
st.set_page_config(page_title="RİSK ÖLÇÜM PLATFORMU", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    /* --- FONT İTHALİ --- */
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&display=swap');

    /* --- GENEL ARKA PLAN --- */
    .stApp {
        background-color: #F8F8F8 !important;
        font-family: 'Manrope', sans-serif !important;
    }

    /* --- SİTE ÇERÇEVESİ (SAYDAM LACİVERT) --- */
    .block-container {
        background: transparent;
        border: 10px solid rgba(10, 25, 47, 0.5); 
        border-radius: 35px;
        padding: 3rem !important;
        margin-top: 2rem;
        box-shadow: 0 0 40px rgba(10, 25, 47, 0.15);
    }

    /* --- BAŞLIK ÇERÇEVESİ --- */
    .header-frame {
        border: 4px solid rgba(10, 25, 47, 0.3);
        background: rgba(10, 25, 47, 0.05);
        backdrop-filter: blur(8px);
        border-radius: 30px;
        padding: 40px 20px;
        text-align: center;
        margin-bottom: 50px;
    }

    /* --- KRİTİK DÜZELTME: INPUT VE SELECTBOX RENKLERİ --- */
    /* Yazı Beyaz, Zemin Lacivert */
    
    /* 1. Normal Yazı ve Sayı Girişleri */
    .stTextInput input, .stNumberInput input {
        background-color: #0a192f !important; /* Lacivert Zemin */
        color: #ffffff !important; /* Beyaz Yazı */
        border: 2px solid #0a192f !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 18px !important; /* Yazı Büyütüldü */
    }

    /* 2. Seçim Kutusu (Selectbox) - Kutunun Kendisi */
    div[data-baseweb="select"] > div {
        background-color: #0a192f !important; /* Lacivert Zemin */
        color: #ffffff !important; /* Beyaz Yazı */
        border-color: #0a192f !important;
        border-radius: 12px !important;
    }
    
    /* Selectbox içindeki seçili metin rengi (SVG ikonlar dahil) */
    div[data-baseweb="select"] span, div[data-baseweb="select"] svg {
        color: #ffffff !important; 
        fill: #ffffff !important;
        font-size: 18px !important; /* Yazı Büyütüldü */
        font-weight: 700 !important;
    }

    /* 3. Açılır Menü Listesi (Dropdown List) */
    div[data-baseweb="popover"], ul[data-baseweb="menu"] {
        background-color: #0a192f !important; /* Listenin arka planı da Lacivert */
    }
    
    /* Liste Elemanları */
    li[role="option"] {
        color: #ffffff !important; /* Liste yazıları Beyaz */
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Mouse ile üzerine gelince (Hover) */
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #1c3146 !important; /* Daha açık lacivert hover */
        font-weight: bold !important;
    }

    /* --- BÜYÜTME: SORULAR VE CEVAPLAR (LABEL & RADIO) --- */
    
    /* Tüm Sorular (Etiketler) */
    label p {
        font-size: 20px !important; /* Sorular büyütüldü */
        font-weight: 800 !important;
        color: #0a192f !important;
        margin-bottom: 10px !important;
    }

    /* Radyo Buton Seçenekleri (Evet/Hayır) */
    .stRadio p, .stCheckbox p {
        font-size: 18px !important; /* Cevaplar büyütüldü */
        font-weight: 600 !important;
        color: #333 !important;
    }

    /* Radyo Buton Arka Planı */
    .stRadio > div {
        background-color: #FAFAFA;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #ddd;
    }

    /* --- KARTLAR --- */
    .design-card {
        background-color: #FFFFFF;
        padding: 40px;
        border-radius: 24px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        border: 1px solid #eee;
    }

    /* --- BUTONLAR --- */
    div.stButton > button {
        background-color: #0a192f !important;
        color: #FFFFFF !important;
        border-radius: 50px !important;
        padding: 20px 40px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        border: none !important;
        width: 100%;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        background-color: #1c3146 !important;
        transform: scale(1.02);
    }

    /* --- BAŞLIKLAR --- */
    .main-title {
        font-size: 4rem !important;
        font-weight: 900 !important;
        color: #0a192f !important;
        margin: 0;
    }
    .sub-title {
        font-size: 1.2rem !important;
        color: #555 !important;
        margin-top: 10px;
    }
    .section-header {
        font-size: 1.6rem !important;
        color: #0a192f !important;
        border-bottom: 3px solid #0a192f;
        padding-bottom: 15px;
        margin-bottom: 25px;
        font-weight: 800 !important;
    }

    /* --- SONUÇ KUTULARI --- */
    .result-box {
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 15px;
        border-left: 10px solid #000;
        background: #fff;
    }
    .res-bad { border-color: #d32f2f; background-color: #ffebee; color: #b71c1c !important; }
    .res-warn { border-color: #fbc02d; background-color: #fffde7; color: #f57f17 !important; }
    .res-good { border-color: #388e3c; background-color: #e8f5e9; color: #1b5e20 !important; }

    /* --- FOOTER --- */
    .footer-container {
        margin-top: 80px;
        padding: 60px 20px;
        background-color: #0a192f;
        color: #FFFFFF !important;
        text-align: center;
        border-top-left-radius: 40px;
        border-top-right-radius: 40px;
    }
    .footer-name { color: #FFFFFF !important; font-size: 24px; font-weight: 800; }
    
    /* --- HARİTA --- */
    .map-frame {
        border-radius: 20px;
        overflow: hidden;
        border: 2px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. HESAPLAMA MOTORU ---
def generate_ultimate_analysis(p):
    report = []
    # YAPI
    if p['yapi'] == "Betonarme":
        report.append({"title": "Yapı Sistemi: Betonarme", "status": "good", "gain": 0, "text": "Binanız beton ve çeliğin kompozit çalışmasıyla ayakta durmaktadır. Doğru projelendirilmiş betonarme yapılar 'Süneklik' yeteneğine sahiptir.", "solution": "Betonun en büyük düşmanı korozyondur. Bodrum katlarda rutubet kontrolü yapın."})
    elif p['yapi'] == "Yığma/Tuğla":
        report.append({"title": "Yapı Sistemi: Yığma Yapı", "status": "bad", "gain": 15, "text": "Yığma yapılar, taşıyıcı duvarlardan oluşur ve 'Gevrek' (Kırılgan) davranış gösterir. Enerji sönümleme kapasitesi düşüktür.", "solution": "Duvarların karbon fiber (FRP) veya çelik hasırlı shotcrete ile güçlendirilmesi önerilir."})
    
    if p['yil'] < 2000:
        report.append({"title": "Yapım Yılı Riski (2000 Öncesi)", "status": "bad", "gain": 20, "text": "Binanız 1999 yönetmeliği öncesi yapılmıştır. Beton kalitesi ve demir donatı standartları günümüz şartlarını sağlamayabilir.", "solution": "Bina performans analizi (Karot testi) yaptırılmalıdır."})
    else:
        report.append({"title": "Modern Yönetmelik Avantajı", "status": "good", "gain": 0, "text": "Binanız modern deprem yönetmelikleriyle inşa edilmiştir.", "solution": "Sonradan yapılan kontrolsüz tadilat olmadığından emin olun."})
    
    if "Z3" in p['zemin'] or "Z4" in p['zemin']:
        report.append({"title": "Zemin Etkisi: Zayıf Zemin", "status": "bad", "gain": 15, "text": "Yumuşak zeminler deprem dalgalarını büyütür (Zemin büyütmesi). Sıvılaşma riski mevcuttur.", "solution": "Zemin iyileştirmesi veya üstyapı güçlendirmesi şarttır."})
    else:
        report.append({"title": "Zemin Etkisi: Sağlam", "status": "good", "gain": 0, "text": "Kayalık veya sert zemin deprem yükünü azaltır.", "solution": "Temel bağlantılarını koruyun."})
    
    if p['kolon'] == "Evet (Şüphe/Kesik)":
        report.append({"title": "KRİTİK HATA: Kolon Müdahalesi", "status": "bad", "gain": 50, "text": "Kolon kesilmesi binanın ani ve toptan yıkımına sebep olur.", "solution": "DERHAL BİNAYI BOŞALTIN ve yetkili mercilere bildirin."})
    
    if p['yumusak'] == "Evet":
        report.append({"title": "Yumuşak Kat Düzensizliği", "status": "bad", "gain": 15, "text": "Zemin kattaki ticari alanlar (yüksek tavan, az duvar) binanın rijitliğini bozar.", "solution": "Çelik çaprazlar ile güçlendirme yapılmalı."})
    
    # İKLİM & ÇEVRE
    if p['iklim'] == "Sert Kış (Karlı/Don)":
        report.append({"title": "Mevsimsel: Hipotermi Riski", "status": "bad", "gain": 10, "text": "Kış şartlarında enkaz dışı hayatta kalma süresi düşer.", "solution": "Termal battaniye ve ısıtıcı ped stoklayın."})
    elif p['iklim'] == "Aşırı Sıcak Yaz":
        report.append({"title": "Mevsimsel: Susuzluk Riski", "status": "warn", "gain": 10, "text": "Sıcakta su ihtiyacı artar.", "solution": "Su stokunu %50 artırın."})
    
    if p['isinma'] == "Doğalgaz":
        if p['vana'] == "Hayır":
            report.append({"title": "Tesisat Riski: Gaz Kaçağı", "status": "bad", "gain": 20, "text": "Depremde gaz sızıntısı ikincil afetlere (yangın) yol açar.", "solution": "Sismik gaz kesici vana taktırın."})
        else:
            report.append({"title": "Tesisat Güvenliği", "status": "good", "gain": 0, "text": "Sismik vananız mevcut.", "solution": "Periyodik bakımını yaptırın."})

    if p['sokak'] == "Dar":
        report.append({"title": "Çevresel: Dar Sokak", "status": "warn", "gain": 10, "text": "Yardım araçları erişimde zorlanabilir.", "solution": "Alternatif kaçış rotası belirleyin."})
    
    if p['egim'] == "Evet":
        report.append({"title": "Jeolojik: Eğimli Arazi", "status": "warn", "gain": 10, "text": "Heyelan veya kaya düşmesi riski.", "solution": "İstinat duvarlarını kontrol ettirin."})

    # SOSYAL
    if p['bebek'] == "Evet":
        report.append({"title": "Sosyal: Bebek Bakımı", "status": "warn", "gain": 10, "text": "Bebek bakımı lojistik zorluk yaratır.", "solution": "Yedek mama, bez ve ilaç stoklayın."})
    if p['hayvan'] == "Evet":
        report.append({"title": "Sosyal: Evcil Hayvan", "status": "warn", "gain": 5, "text": "Hayvanlar panikleyebilir.", "solution": "Taşıma kafesini ve mamasını hazır tutun."})
    if p['engel_var'] == "Evet":
        detay = ", ".join(p['engel_detay'])
        report.append({"title": "Özel Durum: Engelli Birey", "status": "warn", "gain": 15, "text": f"Engel durumu ({detay}) tahliyeyi zorlaştırır.", "solution": "Tahliye sandalyesi edinin ve komşularla plan yapın."})
    if p['arac'] == "Hayır":
        report.append({"title": "Lojistik: Araç Yok", "status": "warn", "gain": 5, "text": "Bölgeden uzaklaşmak zor olabilir.", "solution": "Toplanma alanlarını öğrenin."})

    # HAZIRLIK
    if not p['dask']:
        report.append({"title": "Finansal: DASK Yok", "status": "bad", "gain": 5, "text": "Maddi güvence eksikliği.", "solution": "Hemen sigorta yaptırın."})
    else:
        report.append({"title": "Finansal Güvence", "status": "good", "gain": 0, "text": "DASK poliçeniz mevcut.", "solution": "Her yıl yenileyin."})
    
    if not p['egitim']:
        report.append({"title": "Bilinç Eksikliği", "status": "warn", "gain": 5, "text": "Panik anında yanlış refleks riski.", "solution": "Tatbikat yapın."})
    if not p['plan']:
        report.append({"title": "Planlama Eksikliği", "status": "bad", "gain": 5, "text": "Aile üyelerinin nerede buluşacağı belirsiz.", "solution": "Aile afet planı oluşturun."})
    
    if p['esya'] != "Tamamı":
        report.append({"title": "Yapısal Olmayan Risk: Eşyalar", "status": "bad", "gain": 15, "text": "Yaralanmaların %50'si devrilen eşyalardan kaynaklanır.", "solution": "L Tipi gönyelerle sabitleme yapın."})
    if p['canta'] != "Tam":
        report.append({"title": "Lojistik: Çanta Eksik", "status": "warn", "gain": 10, "text": "İlk 72 saat hayati malzemeler eksik olabilir.", "solution": "Afet çantası hazırlayın."})
    
    return report

def calculate_final_metrics(report):
    base_score = 5.0
    potential_reduction = 0
    for item in report:
        if item['status'] == 'bad':
            base_score += 20
            potential_reduction += item['gain']
        elif item['status'] == 'warn':
            base_score += 10
            potential_reduction += item['gain']
    current_risk = max(5.0, min(99.9, base_score))
    target_risk = max(5.0, min(99.9, current_risk - potential_reduction))
    return current_risk, target_risk

def create_pdf(ad, sehir, risk, target, report):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 15, 'RISK OLCUM RAPORU', 0, 1, 'C')
    tr = lambda x: x.translate(str.maketrans("ğĞıİşŞçÇöÖüÜ", "gGiIsScCoOuU"))
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, txt=tr(f"Hazirlayan: Risk Platformu | Kullanici: {ad} | Konum: {sehir}"), ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=tr(f"MEVCUT RISK: %{risk:.1f}   HEDEF: %{target:.1f}"), ln=True)
    pdf.ln(5)
    for item in report:
        status_color = "[KRITIK]" if item['status'] == 'bad' else "[UYARI]" if item['status'] == 'warn' else "[IYI]"
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 8, txt=tr(f"{status_color} {item['title']}"), ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, txt=tr(item['text']))
        if 'solution' in item and item['solution']:
            pdf.set_font("Arial", 'I', 9)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, txt=tr(f"ONERI: {item['solution']}"))
            pdf.set_text_color(0, 0, 0)
        pdf.ln(3)
    return pdf.output(dest='S').encode('latin-1')

# --- 3. UI TASARIMI ---

# HEADER
st.markdown("""
    <div class="header-frame">
        <h1 class="main-title">RİSK ÖLÇÜM<br>PLATFORMU</h1>
        <div class="sub-title">Bilinçli önlem, hayatta kalmanın ilk adımıdır.</div>
    </div>
""", unsafe_allow_html=True)

p = {}

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # --- KİMLİK KARTI ---
    st.markdown('<div class="design-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">01. Konum & Kimlik</div>', unsafe_allow_html=True)
    
    ad = st.text_input("Adınız Soyadınız", placeholder="Tam adınızı giriniz")
    sehir = st.selectbox("Şehir Seçiniz", ["İstanbul", "Ankara", "İzmir", "Bursa", "Erzurum", "Van", "Diğer"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    coords = {"İstanbul": [41.008, 28.978], "İzmir": [38.423, 27.142], "Erzurum": [39.904, 41.267]}
    sel_coords = coords.get(sehir, [39.0, 35.0])
    
    st.markdown('<div class="map-frame">', unsafe_allow_html=True)
    m = folium.Map(location=sel_coords, zoom_start=11, tiles="CartoDB positron") 
    folium.Marker(sel_coords, popup=sehir).add_to(m)
    st_folium(m, width="100%", height=250)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- ÇEVRE KARTI ---
    st.markdown('<div class="design-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">03. Çevre & Lojistik</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        p['iklim'] = st.selectbox("İklim Koşulları", ["Ilıman / Yağışlı", "Sert Kış (Karlı/Don)", "Aşırı Sıcak Yaz"])
        p['sokak'] = st.selectbox("Sokak Genişliği", ["Geniş", "Dar"])
    with c2:
        p['egim'] = st.radio("Arazi Eğimi", ["Hayır (Düz)", "Evet (Eğimli)"])
        p['egim'] = "Evet" if "Evet" in p['egim'] else "Hayır"
        
    p['arac'] = st.radio("Tahliye Aracınız Var mı?", ["Evet", "Hayır"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- HAZIRLIK KARTI ---
    st.markdown('<div class="design-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">05. Hazırlık Seviyesi</div>', unsafe_allow_html=True)
    
    c_haz1, c_haz2, c_haz3 = st.columns(3)
    with c_haz1: p['dask'] = st.checkbox("DASK Var")
    with c_haz2: p['egitim'] = st.checkbox("Eğitim Aldım")
    with c_haz3: p['plan'] = st.checkbox("Plan Hazır")
    
    st.markdown("<hr style='margin: 20px 0; border: 0; border-top: 1px solid #eee;'>", unsafe_allow_html=True)
    
    p['esya'] = st.select_slider("Eşya Sabitleme Oranı", ["Hiçbiri", "Yarısı", "Tamamı"])
    p['canta'] = st.select_slider("Afet Çantası Durumu", ["Yok", "Eksik", "Tam"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # --- YAPI KARTI ---
    st.markdown('<div class="design-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">02. Bina Analizi</div>', unsafe_allow_html=True)
    
    p['yapi'] = st.selectbox("Yapı Sistemi", ["Betonarme", "Yığma/Tuğla", "Çelik", "Ahşap"])
    p['yil'] = st.number_input("Yapım Yılı", 1950, 2025, 2000)
    p['zemin'] = st.selectbox("Zemin Sınıfı", ["Z1 - Kayalık (Sert)", "Z2 - Sert Toprak", "Z3 - Yumuşak", "Z4 - Dere Yatağı"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_heat1, col_heat2 = st.columns(2)
    with col_heat1:
        p['isinma'] = st.selectbox("Isınma", ["Doğalgaz", "Soba", "Merkezi", "Klima"])
    with col_heat2:
        p['vana'] = st.radio("Sismik Vana", ["Hayır", "Evet"], disabled=p['isinma']!="Doğalgaz")

    st.warning("⚠️ Kritik Kontrol Noktaları")
    p['kolon'] = st.radio("Kolon Müdahalesi (Kesik/Hasarlı)", ["Hayır", "Evet (Şüphe/Kesik)"])
    p['yumusak'] = st.radio("Giriş Kat Dükkan (Yumuşak Kat)", ["Hayır", "Evet"])
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SOSYAL KARTI ---
    st.markdown('<div class="design-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">04. Sosyal Durum</div>', unsafe_allow_html=True)
    
    col_soc1, col_soc2 = st.columns(2)
    with col_soc1:
        p['bebek'] = st.radio("Bebek Var mı?", ["Hayır", "Evet"])
    with col_soc2:
        p['hayvan'] = st.radio("Evcil Hayvan?", ["Hayır", "Evet"])
        
    p['engel_var'] = st.radio("Engelli Birey Var mı?", ["Hayır", "Evet"], horizontal=True)
    p['engel_detay'] = []
    if p['engel_var'] == "Evet":
        p['engel_detay'] = st.multiselect("Engel Türü", ["Hareket", "Zihinsel", "Görme", "İşitme"])
    st.markdown('</div>', unsafe_allow_html=True)

# --- AKSİYON ---
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
if st.button("ANALİZİ BAŞLAT", type="primary", use_container_width=True):
    if not ad:
        st.error("Lütfen rapor için adınızı giriniz.")
    else:
        # Hesaplama
        report = generate_ultimate_analysis(p)
        risk, target = calculate_final_metrics(report)
        
        # Sonuç Ekranı
        st.markdown("---")
        st.markdown("<div class='header-frame'><h2 class='main-title' style='font-size:3rem !important;'>ANALİZ SONUCU</h2></div>", unsafe_allow_html=True)
        
        metric_col1, metric_col2, metric_col3 = st.columns([1,1,1])
        
        with metric_col1:
            st.markdown(f"""
                <div style="background:black; color:white; padding:30px; border-radius:20px; text-align:center;">
                    <div style="font-size:16px; opacity:0.8;">MEVCUT RİSK</div>
                    <div style="font-size:48px; font-weight:800;">%{risk:.1f}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with metric_col2:
            st.markdown(f"""
                <div style="border:2px solid black; color:black; padding:30px; border-radius:20px; text-align:center;">
                    <div style="font-size:16px;">HEDEFLENEN</div>
                    <div style="font-size:48px; font-weight:800;">%{target:.1f}</div>
                    <div style="font-size:12px; font-weight:bold; color:green;">↓ İYİLEŞTİRME: %{risk-target:.1f}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with metric_col3:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk,
                number={'font': {'color': 'black', 'family': 'Manrope'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
                    'bar': {'color': "black"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "black",
                }
            ))
            fig.update_layout(height=160, margin=dict(t=10,b=10,l=10,r=10), paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Manrope'})
            st.plotly_chart(fig, use_container_width=True)

        # Rapor Detayları
        st.markdown("<br><div class='header-frame' style='padding:20px;'><h3 style='text-align:center; margin:0;'>DETAYLI RAPOR</h3></div><br>", unsafe_allow_html=True)
        
        for item in report:
            css_class = "res-bad" if item['status'] == 'bad' else "res-good" if item['status'] == 'good' else "res-warn"
            icon = "🛑" if item['status'] == 'bad' else "✅" if item['status'] == 'good' else "⚠️"
            
            st.markdown(f"""
            <div class="result-box {css_class}">
                <div style="font-size:20px; font-weight:800; color:inherit;">{icon} {item['title']}</div>
                <div style="font-size:18px; margin-top:8px; color:#333;">{item['text']}</div>
                <div style="margin-top:10px; font-size:16px; font-weight:bold; color:black; opacity:0.7;">
                    👉 ÇÖZÜM: {item.get('solution', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # PDF İndir
        pdf_data = create_pdf(ad, sehir, risk, target, report)
        st.download_button(
            label="RAPORU PDF OLARAK İNDİR",
            data=pdf_data,
            file_name=f"risk_raporu_{ad}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# --- FOOTER ---
st.markdown("""
    <div class="footer-container">
        <div class="footer-name">CAN AHMET NAMLI</div>
        <div class="footer-text">Yazılım & Geliştirme</div>
        <div class="footer-text">canahmet1300@gmail.com | 0545 174 1300</div>
        <div style="margin-top:30px; font-size:12px; color:#444;">© 2025 Risk Ölçüm Platformu. Tüm Hakları Saklıdır.</div>
    </div>
""", unsafe_allow_html=True)