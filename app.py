import streamlit as st

# Sayfa Başlığı ve Senaryo Girişi
st.set_page_config(page_title="Müfettiş Berat Görev Başında", layout="centered")
st.title("🕵️‍♂️ Müfettiş Berat Görev Başında")
st.markdown("### Senaryo: 'Gizli Tamlar Fabrikası'")
st.info("Görevimiz siparişlerin tek bir kutuya sığıp sığmayacağını bulmak.")

# Kullanıcı Girişleri (Pay ve Payda)
col1, col2 = st.columns(2)
with col1:
    pay = st.number_input("Sipariş Miktarı (Pay)", min_value=0, value=3, step=1)
with col2:
    payda = st.number_input("Kutu Bölme Sayısı (Payda)", min_value=1, value=4, step=1)

st.write(f"### Sipariş: {pay} / {payda}")

# Uygulama ve Soru Bölümü
st.markdown("---")
st.markdown(f"**Uygulama:** {payda} bölmeli kutuya {pay} tane eşya yerleştirilir.")

# Bilişsel Kodlama ve Mantık
if pay < payda:
    # Durum A: Basit Kesir (Sığan Kesir)
    st.success("✅ Berat, kutuda boş yer kaldı! Eşyalar dışarı taşmadı.")
    st.markdown("### 📝 Bilişsel Kodlama:")
    st.write("Eşyalar (Pay), bölmelerden (Payda) azsa bu **Basit Kesirdir**.")
    st.write("> 'Kutuya sığdı, miktar 1 bütünden az'.")
else:
    # Durum B: Bileşik Kesir (Taşan Kesir)
    st.error("⚠️ Eyvah! Eşyalar dışarı taştı!")
    st.markdown("### 📝 Bilişsel Kodlama:")
    st.write("Eşyalar (Pay), bölmelerden (Payda) fazla veya ona eşitse bu **Bileşik Kesirdir**.")
    st.write("> 'Kutuya sığmadı, 1 bütün veya daha fazlasına ihtiyacımız var'.")

# Görselleştirme
st.markdown("---")
st.markdown("**Kutu Görünümü:**")
slots = ""
for i in range(max(pay, payda)):
    if i < pay:
        slots += "🍎 " # Eşya
    else:
        slots += "⬜ " # Boş Bölme
    
    # Kutu sınırını göster
    if (i + 1) % payda == 0:
        slots += " | "

st.subheader(slots)
