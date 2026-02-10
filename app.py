import streamlit as st
import streamlit.components.v1 as components
import random

# --- KODLAMA STANDARTLARI: KONFİGÜRASYON ---
st.set_page_config(page_title="Gizli Tamlar Fabrikası v3", layout="wide")

# --- SİPARİŞ KARTLARI (Dinamik Seçenekler) ---
SİPARİŞLER = [
    {"pay": 7, "payda": 3, "etiket": "7/3 (Standart)"},
    {"pay": 13, "payda": 4, "etiket": "13/4 (Büyük Sipariş)"},
    {"pay": 5, "payda": 2, "etiket": "5/2 (Hızlı Üretim)"},
    {"pay": 10, "payda": 6, "etiket": "10/6 (Hassas Kesim)"}
]

# --- SESSION STATE (DURUM YÖNETİMİ) ---
if 'aktif_siparis' not in st.session_state:
    st.session_state.aktif_siparis = SİPARİŞLER[0]

# --- SIDEBAR: FABRİKA YÖNETİMİ ---
with st.sidebar:
    st.header("📋 Fabrika Kontrol Paneli")
    secim = st.selectbox(
        "Sipariş Kartı Seçin:",
        options=range(len(SİPARİŞLER)),
        format_func=lambda x: SİPARİŞLER[x]["etiket"]
    )
    
    if st.button("🚀 Yeni Siparişi İşle"):
        st.session_state.aktif_siparis = SİPARİŞLER[secim]
        st.rerun()
    
    st.markdown("---")
    st.info("**Eğitim Notu:** Bu uygulama Piaget'nin 'Korunum' ilkesini temel alır. Parçalar paketlense bile toplam miktar (sayılı sayaç) değişmez.")

# --- HTML/JS/CSS MOTORU ---
# f-string hata yönetimi için tüm süslü parantezler {{ }} şeklinde çiftlenmiştir.
order_num = st.session_state.aktif_siparis["pay"]
order_den = st.session_state.aktif_siparis["payda"]

html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        :root {{
            --primary: #0984e3;
            --accent: #ff7675;
            --bg: #fdfdfd;
            --shipping-area: #e8f8f5;
        }}
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--bg); display: flex; flex-direction: column; align-items: center; padding: 10px; }}
        
        /* SİPARİŞ KARTI (image_2b925a referanslı tipografi) */
        .order-card {{
            background: white; border: 3px dashed var(--accent); border-radius: 12px;
            padding: 10px; width: 280px; text-align: center; margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }}
        .order-num {{ font-size: 38px; font-weight: bold; color: var(--accent); margin: 0; }}
        .order-line {{ border-bottom: 4px solid var(--accent); width: 35px; margin: 4px auto; }}
        .order-den {{ font-size: 28px; font-weight: bold; color: var(--accent); margin: 0; }}

        /* FABRİKA DÜZENİ */
        .factory-grid {{
            display: grid; grid-template-columns: 1.2fr 220px 1.8fr;
            gap: 15px; width: 100%; max-width: 1150px; align-items: stretch;
        }}

        .section-box {{
            background: white; border: 2px solid #eee; border-radius: 15px; padding: 15px;
            display: flex; flex-direction: column; min-height: 380px; position: relative;
        }}
        
        /* BAŞLIKLAR (image_2b925a'daki gibi içeriği kapatmayan üst yerleşim) */
        .section-title {{ 
            font-size: 11px; color: #aaa; font-weight: 800; text-align: center; 
            text-transform: uppercase; margin-bottom: 25px; letter-spacing: 1.2px;
            border-bottom: 1px solid #f1f1f1; padding-bottom: 5px;
        }}

        /* BİRİM KESİRLER */
        .pool {{ display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; }}
        .piece {{
            width: 45px; height: 45px; background: var(--primary); color: white;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; cursor: pointer; border-radius: 6px; font-size: 11px;
            transition: 0.2s; border: 1px solid rgba(255,255,255,0.2);
        }}
        .piece:hover {{ transform: translateY(-3px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}

        /* MAKİNE (BİRİKİMLİ SAYAÇ) */
        .machine-unit {{
            display: flex; flex-direction: column; align-items: center; 
            border: 2px solid #fab1a0; background: #fffcfb; border-radius: 10px; padding: 10px; height: 100%;
        }}
        #birikimli-sayac {{
            font-size: 20px; font-weight: 900; color: var(--primary); 
            background: #e1f5fe; padding: 6px 18px; border-radius: 30px; margin-bottom: 15px;
            border: 1px solid #b3e5fc;
        }}
        .conveyor-belt {{
            width: 100%; border: 2px dashed #ddd; border-radius: 8px; 
            min-height: 70px; display: flex; flex-wrap: wrap; align-items: center; 
            justify-content: center; gap: 3px; padding: 5px;
        }}

        /* SEVKİYAT (SAĞ) */
        .shipping {{ background: var(--shipping-area); border-color: #00b894; }}
        .shipping-dock {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }}
        
        .box-product {{
            display: flex; border: 2px solid #e17055; background: #ffeaa7;
            border-radius: 6px; position: relative; padding: 3px; height: 50px; align-items: center;
            animation: bounceIn 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }}
        .box-product::after {{
            content: "1 TAM"; position: absolute; top: -18px; left: 50%; transform: translateX(-50%);
            background: #e17055; color: white; padding: 1px 7px; border-radius: 10px; font-size: 9px; font-weight: bold;
        }}
        
        .rem-product {{
            background: #a29bfe; border: 2px solid #6c5ce7; border-radius: 6px; 
            padding: 3px; height: 50px; display: flex; align-items: center; position: relative;
            animation: fadeIn 0.5s ease;
        }}
        .rem-product::after {{
            content: "ARTAN"; position: absolute; top: -18px; left: 50%; transform: translateX(-50%);
            background: #6c5ce7; color: white; padding: 1px 7px; border-radius: 10px; font-size: 9px; font-weight: bold;
        }}

        .packed-mini {{ width: 38px; height: 38px; background: var(--primary); border: 1px solid white; display: flex; align-items: center; justify-content: center; color: white; font-size: 9px; font-weight: bold; }}

        @keyframes bounceIn {{ 0% {{ transform: scale(0.3); opacity: 0; }} 100% {{ transform: scale(1); opacity: 1; }} }}
    </style>
</head>
<body>

    <div class="order-card">
        <div style="font-size: 9px; color: #aaa; letter-spacing: 1px;">SİPARİŞ KARTI</div>
        <p class="order-num">{order_num}</p>
        <div class="order-line"></div>
        <p class="order-den">{order_den}</p>
    </div>

    <div class="factory-grid">
        <div class="section-box">
            <div class="section-title">1. Ham Madde Deposu</div>
            <div class="pool" id="depo"></div>
        </div>

        <div class="section-box">
            <div class="section-title">2. Makine (Üretim)</div>
            <div class="machine-unit">
                <div id="birikimli-sayac">0 / {order_den}</div>
                <div class="conveyor-belt" id="belt"></div>
            </div>
        </div>

        <div class="section-box shipping">
            <div class="section-title">3. Sevkiyat Alanı (Ürünler)</div>
            <div class="shipping-dock" id="dock"></div>
        </div>
    </div>

    <script>
        const payda = {order_den};
        const toplamPay = {order_num};
        let toplamIslenen = 0; // Birikimli Sayaç (Sıfırlanmaz!)
        let aktifKutuIci = 0; // Paketleme için geçici sayaç

        const depoDiv = document.getElementById('depo');
        const beltDiv = document.getElementById('belt');
        const dockDiv = document.getElementById('dock');
        const sayacDisplay = document.getElementById('birikimli-sayac');

        function depoYukle() {{
            for(let i=0; i < toplamPay; i++) {{
                let p = document.createElement('div');
                p.className = 'piece';
                p.innerText = '1/' + payda;
                p.onclick = () => islemYap(p);
                depoDiv.appendChild(p);
            }}
        }}

        function islemYap(el) {{
            depoDiv.removeChild(el);
            
            // 1. SAYAÇ GÜNCELLEME (BİRİKİMLİ)
            toplamIslenen++;
            sayacDisplay.innerText = toplamIslenen + " / " + payda;

            // 2. MAKİNE GÖRSELİ
            aktifKutuIci++;
            let mini = document.createElement('div');
            mini.className = 'packed-mini';
            mini.innerText = '1/' + payda;
            beltDiv.appendChild(mini);

            // 3. PAKETLEME KONTROLÜ (OTOMATİK TAM)
            if (aktifKutuIci === payda) {{
                setTimeout(gonderTamPaket, 400);
            }} else if (toplamIslenen === toplamPay) {{
                // Sipariş bitti ama tam paket olamadı (Artan)
                setTimeout(gonderArtanParca, 600);
            }}
        }}

        function gonderTamPaket() {{
            let kutu = document.createElement('div');
            kutu.className = 'box-product';
            for(let i=0; i < payda; i++) {{
                let p = document.createElement('div');
                p.className = 'packed-mini';
                p.innerText = '1/' + payda;
                kutu.appendChild(p);
            }}
            dockDiv.appendChild(kutu);
            
            // Görseli temizle, sayacı koru
            beltDiv.innerHTML = '';
            aktifKutuIci = 0;
            
            confetti({{ particleCount: 70, spread: 60, origin: {{ x: 0.7, y: 0.6 }} }});
        }}

        function gonderArtanParca() {{
            if (aktifKutuIci > 0) {{
                let artanKutu = document.createElement('div');
                artanKutu.className = 'rem-product';
                for(let i=0; i < aktifKutuIci; i++) {{
                    let p = document.createElement('div');
                    p.className = 'packed-mini';
                    p.innerText = '1/' + payda;
                    artanKutu.appendChild(p);
                }}
                dockDiv.appendChild(artanKutu);
                beltDiv.innerHTML = '';
                aktifKutuIci = 0;
                sayacDisplay.innerText = "Sipariş Tamam!";
            }}
        }}

        depoYukle();
    </script>
</body>
</html>
"""

components.html(html_code, height=780)
