import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class FractionModeler:
    """Kesir hesaplamaları ve görselleştirmeyi yöneten ana sınıf."""
    
    @staticmethod
    def get_details(num: int, den: int):
        """Kesir tipini ve tam sayılı dönüşümünü hesaplar."""
        if den == 0:
            return None
        
        fraction_type = "Basit Kesir" if num < den else "Bileşik Kesir"
        whole = num // den
        remainder = num % den
        return {
            "type": fraction_type,
            "whole": whole,
            "remainder": remainder,
            "is_mixed": whole > 0 and remainder > 0
        }

    @staticmethod
    def draw_model(num: int, den: int):
        """Kesri dikdörtgen modeller (bloklar) halinde çizer."""
        # Kaç tam blok çizilmesi gerektiğini hesapla
        needed_blocks = (num // den) + (1 if num % den != 0 else 0)
        if num == 0: needed_blocks = 1

        # Grafik ayarları
        fig, axes = plt.subplots(needed_blocks, 1, figsize=(8, 2 * needed_blocks))
        if needed_blocks == 1: axes = [axes]

        temp_num = num
        for i in range(needed_blocks):
            ax = axes[i]
            for j in range(den):
                # Parça boyalı mı değil mi kontrolü
                fill_color = "orange" if temp_num > 0 else "white"
                rect = patches.Rectangle((j, 0), 1, 1, linewidth=2, edgecolor='black', facecolor=fill_color)
                ax.add_patch(rect)
                temp_num -= 1
            
            ax.set_xlim(0, den)
            ax.set_ylim(0, 1)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(f"Bütün {i+1}", loc='left', fontsize=10, color='#555')

        plt.tight_layout()
        return fig

def main():
    # Streamlit Sayfa Ayarları
    st
