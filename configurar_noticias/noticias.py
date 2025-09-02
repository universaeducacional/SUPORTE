import streamlit as st

st.title("🎬 Portal YouTube Interativo")

# campo de entrada pro usuário
url = st.text_input("Cole aqui o link do YouTube:")

# botão para abrir
if st.button("Abrir vídeo"):
    if url.strip():
        st.success("✅ Vídeo carregado com sucesso!")
        # Embed direto no Streamlit
        st.video(url)
        # Botão para abrir em uma nova aba
        st.link_button("Abrir no YouTube", url)
    else:
        st.error("⚠️ Cole um link válido do YouTube primeiro!")
