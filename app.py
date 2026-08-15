import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Audio Transcriptor AI", layout="wide")

st.title("🎤 Transcriptor de Audio + IA")

with st.sidebar:
    st.header("⚙️ Configuración")
    claude_key = st.text_input("🔑 Token Claude:", type="password")
    action = st.radio("¿Qué hacer?", ["📝 Transcribir", "📋 Resumir", "✅ Acciones"])

st.header("1️⃣ Tu Audio")
uploaded_file = st.file_uploader("Sube audio", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.success("✅ Archivo cargado")
    
    st.header("2️⃣ Transcripción")
    transcription_text = st.text_area("Pega transcripción:", height=150)
    
    if transcription_text and claude_key:
        st.header("3️⃣ Procesar")
        
        if st.button("🚀 Procesar"):
            try:
                from anthropic import Anthropic
                
                client = Anthropic(api_key=claude_key)
                
                if action == "📝 Transcribir":
                    msg = transcription_text
                elif action == "📋 Resumir":
                    msg = f"Resume esto en 3 puntos:\n{transcription_text}"
                else:
                    msg = f"Extrae acciones de esto:\n{transcription_text}"
                
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=500,
                    messages=[{"role": "user", "content": msg}]
                )
                
                result = response.content[0].text
                st.success("✅ Listo!")
                st.write(result)
                
                st.download_button(
                    "📥 Descargar",
                    result,
                    file_name=f"resultado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                )
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown("Audio + IA por C l a u d e ☁️")
