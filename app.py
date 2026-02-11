import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import logging

# --- LOGGING YAPILANDIRMASI ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- MODEL VE MANTIK KATMANI (Logic Layer) ---
class FractionManager:
    """Kesir hesaplamaları ve türlerini yöneten sınıf."""
    
    @staticmethod
    def identify_type(num: int, den: int) -> str:
        """Kesrin matematiksel türünü belirler."""
        if den == 0:
            raise ValueError("Matematiksel hata: Payda 0 olamaz.")
        
        if abs(num) < abs(den):
            return "Basit Kesir"
        else:
            return "Bileşik Kesir"

    @staticmethod
    def get_mixed_representation(num: int, den: int):
        """Bileşik kesri tam sayılı kesir parçalarına ayırır."""
        try:
            whole = num // den
            remainder = num % den
            return whole, remainder
        except ZeroDivisionError:
            return 0, 0

# --- GÖRSELLEŞTİRME KATMANI (Visualization Layer) ---
class FractionPainter:
    """Matplotlib kullanarak kesirleri görselleştiren sınıf."""

    @staticmethod
    def create_block_model(num: int, den: int):
        """Dikdörtgen bloklar üzerinde kesri modeller."""
        # Toplam kaç bütün (kutu) çizilmeli?
        total_blocks = (num // den) + (1 if num % den != 0 else 0)
        if total_blocks == 0 and num > 0: total_blocks = 1
        
        # Grafik ayarları
        fig, axes = plt.subplots(total_blocks, 1, figsize=(8, 2 * total_blocks))
        if total_blocks == 1:
            axes = [axes]

        current_num = num
        for i in range(total_blocks):
            ax = axes[i]
            for d in range(den):
                # Eğer kalan pay varsa kutuyu boya
                color = "#3498db" if current_num > 0 else "#ecf0f1"
                ax.add_patch(plt.Rectangle((d, 0), 1, 1, facecolor=color, edgecolor="#2c3e50", linewidth=1.5))
                current_num -= 1
            
            ax.set_xlim(0, den)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(f"{i+1}. Bütün (Payda: {den} Parça)", fontsize=9, loc='left', color='#7f8c8d')

        plt.tight_layout()
        return fig

# --- KULLANICI ARAYÜZÜ (UI Layer - Streamlit) ---
def run_app():
    # Sayfa Konfigürasyonu
    st.set_page_config(
        page_title="Kesir Modelleme Uzmanı",
        page_icon="📏",
        layout="wide"
    )

    # Başlık ve Açıklama
    st.title("📏 İnteraktif Kesir Modelleme")
    st.markdown("""
    Bu uygulama, matematiksel kesirleri (Basit, Bileşik ve Tam Sayılı) 
    **görsel bloklar** halinde modeller. Değerleri değiştirerek farkı keşfedin!
    """)

    st.sidebar.header("🔢 Giriş Paneli")
    
    # Güvenli Girdi Yönetimi
    with st.sidebar:
        numerator = st.number_input("Pay (Üst Kısım)", min_value=0, max_value=100, value=7, step=1)
        denominator = st.number_input("Payda (Alt Kısım)", min_value=1, max_value=20, value=4, step=1)
        st.info("💡 Not: Performans için pay 100, payda 20 ile sınırlandırılmıştır.")

    try:
        # Hesaplamaları Yap
        f_type = FractionManager.identify_type(numerator, denominator)
        whole_part, rem_part = FractionManager.get_mixed_representation(numerator, denominator)

        # Dashboard Alanı
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Girdi", f"{numerator} / {denominator}")
        
        with col2:
            st.metric("Kesir Türü", f_type)
            
        with col3:
            if f_type == "Bileşik Kesir":
                mixed_str = f"{whole_part} Tam {rem_part}/{denominator}"
                st.metric("Tam Sayılı Dönüşüm", mixed_str)
            else:
                st.metric("Tam Sayılı Dönüşüm", "N/A (Basit Kesir)")

        # Görselleştirme Bölümü
        st.divider()
        st.subheader("🖼️ Görsel Model")
        
        with st.spinner('Model çiziliyor...'):
            fig = FractionPainter.create_block_model(numerator, denominator)
            st.pyplot(fig)
            
        # Analiz Notu
        with st.expander("📝 Bu modeli nasıl okumalıyım?"):
            st.write(f"""
            - Her bir büyük dikdörtgen **1 tam** bütünü temsil eder.
            - Her bütün, payda değeriniz olan **{denominator}** eşit parçaya bölünmüştür.
            - Toplamda **{numerator}** adet küçük parça maviye boyanmıştır.
            - Boyanan parçalar birden fazla bütünü dolduruyorsa, bu bir **Bileşik Kesirdir**.
            """)

    except Exception as e:
        logger.error(f"Uygulama hatası: {str(e)}")
        st.error(f"Beklenmedik bir hata oluştu. Lütfen girdileri kontrol edin.")

if __name__ == "__main__":
    run_app()
