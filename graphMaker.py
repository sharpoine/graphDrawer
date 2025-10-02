# dosya: app.py
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Graf Çizici", layout="centered")
st.title("Graf Çizici")

st.markdown("""
Bu uygulama farklı dizilim seçenekleri ile graflar oluşturup png olarak indirme olanak sağlar.
""")

st.markdown("---")  # yatay çizgi
st.markdown("Coded by **Eren Özel** 212709067  @Student of **Selçuk Üniversitesi**")
# ----------------------------
# Kullanıcı girişleri
# ----------------------------
st.subheader("Noktalar ve Kenarlar")
dugumler_input = st.text_area("Noktaları virgülle girin (örn: A,B,C,D)", "A,B,C,D")
kenarlar_input = st.text_area("Kenarları girin (örn: A-B,A-C,B-C)", "A-B,A-C,B-C")

dugumler = [d.strip() for d in dugumler_input.split(",") if d.strip()]
kenarlar = [tuple(k.strip().split("-")) for k in kenarlar_input.split(",") if "-" in k.strip()]

# ----------------------------
# Renk ve boyut seçenekleri
# ----------------------------


st.subheader("Görünüm Seçenekleri")
node_color = st.color_picker("Nokta Rengi", "#87CEEB")
edge_color = st.color_picker("Kenar Rengi", "#808080")
node_size = st.slider("Nokta Boyutu", 200, 1500, 800)
font_size = st.slider("Yazı Boyutu", 6, 24, 12)

st.info("""
**Layout Açıklamaları:** 
- **spring**: Noktalar birbirini itip çeker gibi yerleşir (force-directed), en yaygın ve dengeli layout.
- **circular**: Noktalar bir daire üzerinde yerleştirilir.        
- **kamada_kawai**: Spring benzeri, ama daha optimize edilmiş, noktalar arasındaki mesafeyi korur.
- **random**: Noktalar rastgele konumlandırılır.
- **shell**: Noktalar bir veya birden fazla halka (shell) üzerinde yerleştirilir.
- **spectral**: Laplacian matrisinin eigenvector’larına göre yerleştirir, spektral graf teorisi için uygundur.
""")
layout_option = st.selectbox("Graf Layout", ["spring", "circular", "kamada_kawai", "random", "shell", "spectral"])



# ----------------------------
# Grafı çizme ve gösterme
# ----------------------------


#spring_layout	Düğümler birbirini itip çeker gibi yerleşir (force-directed), en yaygın ve dengeli layout.
#circular_layout	Düğümler bir daire üzerinde yerleştirilir.
#kamada_kawai_layout	Spring benzeri, ama daha optimize edilmiş, düğümler arasındaki mesafeyi korur.
#random_layout	Düğümler rastgele konumlandırılır.
#shell_layout	Düğümler bir veya birden fazla halka (shell) üzerinde yerleştirilir.#
#spectral_layout	Laplacian matrisinin eigenvector’larına göre yerleştirir, spektral graf teorisi için uygundur.
#multipartite_layout	Çok parçalı graf (partite) için katmanlı yerleşim sağlar.
if st.button("🎨 Grafı Çiz ve Göster"):
    if len(dugumler) > 0 and len(kenarlar) > 0:
        G = nx.Graph()
        G.add_nodes_from(dugumler)
        G.add_edges_from(kenarlar)


        if layout_option == "spring":
            pos = nx.spring_layout(G)
        elif layout_option == "shell":
            pos = nx.shell_layout(G)
        elif layout_option == "spectral":
            pos = nx.spectral_layout(G)
        elif layout_option == "circular":
            pos = nx.circular_layout(G)
        elif layout_option == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.random_layout(G)

        # Graf çizimi
        plt.figure(figsize=(6,6))
        nx.draw(G, pos,
                with_labels=True,
                node_color=node_color,
                edge_color=edge_color,
                node_size=node_size,
                font_size=font_size)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=300)
        plt.close()
        st.image(buf, width='stretch')
        st.download_button("⬇️ PNG Olarak İndir", data=buf.getvalue(),
                           file_name="graf.png", mime="image/png")
    else:
        st.warning("Lütfen nokta ve kenarları doğru şekilde girin!")
