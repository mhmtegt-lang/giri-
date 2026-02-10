import streamlit as st
import math

# ==========================================
# 1. AYARLAR VE STİL (CSS)
# ==========================================
st.set_page_config(
    page_title="Gizli Tamlar Fabrikası",
    page_icon="🏭",
    layout="wide"
)

def yerel_css_yukle():
    """Uygulama içi görselleştirmeler için CSS stilleri."""
    st.markdown("""
        <style>
        .factory-box {
            border: 3px solid #333;
            border-radius: 10px;
            padding: 10px;
            margin: 5px;
            background-color: #f9f9f9;
            text-align: center;
            display: inline-block;
            width: 150px;
        }
        .slot {
            display: inline-block;
            width: 25px;
            height: 25px;
            border: 1px dashed #aaa;
            border-radius: 50%;
            margin: 2px;
            background-color: white;
            line-height: 25px;
            font-size: 14px;
        }
        .filled {
            background-color: #ff4b4b;
            border: 1px solid #c0392b;
            color: white;
        }
        .info-card {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 5px solid;
        }
        .success { background-color: #e6fffa; border-color: #38b2ac; color: #234e52; }
        .warning { background-color: #fffaf0; border-color: #ed8936; color: #7b341e; }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. İŞ MANTIĞI (LOGIC CLASS)
# ==========================================
class KesirMufettisi:
    """Piaget'nin Odaktan Uzaklaşma ilkesine göre kesir analizi yapar."""
    
    def __init__(self, pay, payda):
        self.pay = pay
        self.payda = payda
        
    def analiz_et(self):
        """Kesrin durumunu hesaplar ve rapor döner."""
        if self.payda == 0:
            return {"hata": "Payda 0 olamaz!"}
            
        tam_kutu_sayisi = self.pay // self.payda
        kalan_urun = self.pay % self.payda
        gerekli_toplam_kutu = math.ceil(self.pay / self.payda)
        
        # Hiç ürün yoksa bile boş bir kutu gösterelim
        if gerekli_toplam_kutu == 0:
            gerekli_toplam_kutu = 1

        basit_kesir_mi = self.pay < self.payda
        
        return {
            "tip": "Basit Kesir (Sığan)" if basit_kesir_mi else "Bileşik Kesir (Taşan)",
            "mesaj": "Kutuya sığdı, 1 bütünden az." if basit_kesir_mi else "Kutuya sığmadı, taştı!",
            "tasti_mi": not basit_kesir_mi,
            "toplam_kutu": gerekli_toplam_kutu,
            "kalan": kalan_urun
        }

# ==========================================
# 3. GÖRSELLEŞTİRME FONKSİYONLARI
# ==========================================
def kutulari_ciz(toplam_kutu, kutu_kapasitesi, toplam_urun):
    """HTML kullanarak kutuları ve içindeki elmaları çizer."""
    html_cikti = "<div style='display: flex; flex-wrap: wrap; gap: 10px;'>"
    
    kalan_urun = toplam_urun
    
    for i in range(toplam_kutu):
        html_cikti += f"<div class='factory-box'><b>📦 Kutu {i+1}</b><br>"
        
        # Kutunun içindeki slotları çiz
        for _ in range(kutu_kapasitesi):
            if kalan_urun > 0:
                html_cikti += "<span class='slot filled'>🍎</span>"
                kalan_urun -= 1
            else:
                html_cikti += "<span class='slot'>⚪</span>"
                
        html_cikti += "</div>"
    
    html_cikti += "</div>"
    st.markdown(html_cikti, unsafe_allow_html=True)

# ==========================================
# 4. ANA UYGULAMA (MAIN)
# ==========================================
def main():
    yerel_css_yukle()
    
    st.title("🏭 Müfettiş Berat: Görev Başında")
    st.markdown("---")

    # --- Sidebar: Kontrol Paneli ---
    with st.sidebar:
        st.header("📝 Sipariş Paneli")
        pay = st.number_input("Sipariş (Pay)", min_value=0, value=3, step=1)
        payda = st.number_input("Kutu Bölmesi (Payda)", min_value=1, value=4, step=1)
        
        st.metric(label="Oluşan Kesir", value=f"{pay} / {payda}")

    # --- Ana Ekran: Analiz ---
    mufettis = KesirMufettisi(pay, payda)
    sonuc = mufettis.analiz_et()

    if "hata" in sonuc:
        st.error(sonuc["hata"])
    else:
        # Rapor Kısmı
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📋 Durum Raporu")
            css_class = "warning" if sonuc["tasti_mi"] else "success"
            
            st.markdown(f"""
                <div class='info-card {css_class}'>
                    <h3>{sonuc['tip']}</h3>
                    <p>{sonuc['mesaj']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.info(f"**Bilişsel Not:**\nEşyalar ({pay}), bölmelerden ({payda}) {'FAZLA' if sonuc['tasti_mi'] else 'AZ'}.")

        # Görselleştirme Kısmı
        with col2:
            st.subheader("🏭 Üretim Bandı")
            kutulari_ciz(sonuc["toplam_kutu"], payda, pay)

if __name__ == "__main__":
    main()
