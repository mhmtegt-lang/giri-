import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import logging
import sys

# --- CONFIGURATION & LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# --- BUSINESS LOGIC LAYER ---
class FractionLogic:
    """Kesirlerin matematiksel analizini yapan sınıf."""
    @staticmethod
    def analyze(numerator: int, denominator: int):
        if denominator == 0:
            raise ValueError("Payda 0 olamaz! Bir bütünü sıfıra bölemezsiniz.")
        
        is_improper = numerator >= denominator
        whole_part = numerator // denominator
        remainder = numerator % denominator
        
        return {
            "is_improper": is_improper,
            "whole_part": whole_part,
            "remainder": remainder,
            "type": "Bileşik Kesir" if is_improper else "Basit Kesir"
        }

# --- VISUALIZATION LAYER ---
class FractionVisualizer:
    """Matplotlib ile dikdörtgen modellemesi yapan sınıf."""
    @staticmethod
    def draw(numerator: int, denominator: int, is_mixed_view: bool = False):
        try:
            full_boxes = numerator // denominator
            remainder = numerator % denominator
            # Kaç tane dikdörtgen çizilecek?
            total_rects = full_boxes + (1 if remainder > 0 else 0)
            if total_rects == 0: total_rects = 1

            # Grafik alanı ayarları
            fig, ax = plt.subplots(figsize=(8, total_rects * 1.5))
            ax.set_xlim(0, 1.2)
            ax.set_ylim(0, total_rects * 1.1)
            ax.axis('off')

            for i in range(total_rects):
                # Y ekseni pozisyonu (üstten aşağı dizilim)
                y_pos = (total_rects - 1 - i) * 1.1
                
                # 1. Ana Dikdörtgen (Kutu)
                rect = patches.Rectangle((0.1, y_pos), 1.0, 0.8, linewidth=2.5, 
                                       edgecolor='#2C3E50', facecolor='none', zorder=2)
                ax.add_patch(rect)

                # 2. Bölme Çizgileri (Payda kadar)
                for d in range(1, denominator):
                    x_line = 0.1 + (d / denominator)
                    ax.plot([x_line, x_line], [y_pos, y_pos + 0.8], 
                            color='#BDC3C7', lw=1, ls='--', zorder=1)

                # 3. Boyama (Müfettişin Eşyaları)
                if i < full_boxes:
                    # Tam dolu kutular
                    color = '#27AE60' if is_mixed_view else '#2980B9'
                    full_fill = patches.Rectangle((0.1, y_pos), 1.0, 0.8, 
                                                facecolor=color, alpha=0.5, zorder=0)
                    ax.add_patch(full_fill)
                    
                    label = "1 TAM" if is_mixed_view else f"{denominator}/{denominator}"
                    ax.text(0.6, y_pos + 0.35, label, fontsize=12, 
                            fontweight='bold', ha='center', color='#2C3E50')
                
                elif i == full_boxes and remainder > 0:
                    # Artan parçaların olduğu kutu
                    fill_width = remainder / denominator
                    part_fill = patches.Rectangle((0.1, y_pos), fill_width, 0.8, 
                                                facecolor='#E67E22', alpha=0.5, zorder=0)
                    ax.add_patch(part_fill)
                    ax.text(0.1 + fill_width/2, y_pos + 0.35, f"{remainder}/{denominator}", 
                            fontsize=10, fontweight='bold', ha='center')

            plt.tight_layout()
            return fig
        except Exception as e:
            logger.error(f"Görselleştirme hatası: {e}")
            return None

# --- UI / APPLICATION LAYER ---
class InspectorBeratApp:
    """Streamlit uygulamasının ana yönetimi."""
    def __init__(self):
        st.set_page_config(page_title="Müfettiş Berat | Kesir Fabrikası", layout="wide")
        self.logic = FractionLogic()
        self.viz = FractionVisualizer()

    def run(self):
        st.title("🕵️‍♂️ Müfettiş Berat: Dikdörtgen Modelleme Fabrikası")
        st.markdown("---")

        # Sidebar Girdileri
        st.sidebar.header("📦 Sipariş Girişi")
        pay = st.sidebar.number_input("Pay (Eşya Sayısı)", min_value=1, max_value=30, value=5)
        payda = st.sidebar.number_input("Payda (Kutu Bölmesi)", min_value=1, max_value=12, value=4)

        try:
            data = self.logic.analyze(pay, payda)
            
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Bileşik Kesir Modeli")
                st.markdown(f"**Gösterim:** $\\frac{{{pay}}}{{{payda}}}$")
                fig1 = self.viz.draw(pay, payda, is_mixed_view=False)
                if fig1: st.pyplot(fig1)
                
                if data["is_improper"]:
                    st.warning(f"Bu bir **{data['type']}**. Kutular taştı!")
                else:
                    st.success(f"Bu bir **{data['type']}**. Tek kutuya sığdı.")

            with col2:
                st.subheader("📦 Tam Sayılı Model")
                if data["is_improper"]:
                    st.markdown(f"**Gösterim:** ${data['whole_part']} \\frac{{{data['remainder']}}}{{{payda}}}$")
                    fig2 = self.viz.draw(pay, payda, is_mixed_view=True)
                    if fig2: st.pyplot(fig2)
                    st.info(f"**Rapor:** {data['whole_part']} tam kutu doldu, {data['remainder']} parça arttı.")
                else:
                    st.info("Basit kesirlerde tam kısım bulunmaz (0 Tam).")
                    fig1_alt = self.viz.draw(pay, payda, is_mixed_view=False)
                    if fig1_alt: st.pyplot(fig1_alt)

        except Exception as e:
            logger.error(f"Uygulama hatası: {e}")
            st.error("Bir hata oluştu. Lütfen değerleri kontrol edin.")

# --- ENTRY POINT ---
if __name__ == "__main__":
    app = InspectorBeratApp()
    app.run()
