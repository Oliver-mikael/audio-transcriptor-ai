import streamlit as st
import os
from datetime import datetime

# Configuración
st.set_page_config(page_title="Audio Transcriptor AI", layout="wide")

st.title("🎤 Transcriptor de Audio + IA")
st.markdown("Sube audio → Procesa con IA")

# ============================================
# SIDEBAR - Configuración
# ============================================
with st.sidebar:
    st.header("⚙️ Configuración")
    
    claude_key = st.text_input(
        "🔑 Token Claude API:",
        type="password",
        help="Obten en: https://console.anthropic.com/"
    )
    
    action = st.radio(
        "¿Qué quieres hacer?",
        ["📝 Solo transcribir",
         "📋 Resumir",
         "🏷️ Clasificar",
         "✅ Extraer acciones",
         "🔍 Análisis completo"]
    )

# ============================================
# MAIN
# ============================================
st.header("1️⃣ Sube tu Audio")

uploaded_file = st.file_uploader(
    "Sube un archivo de audio",
    type=["mp3", "wav", "m4a", "ogg", "flac"]
)

if uploaded_file:
    st.success("✅ Archivo cargado")
    
    # Guardar archivo
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("⚠️ Para transcribir, necesitas usar un servicio externo o Whisper API")
    
    # Simulación de transcripción (para demo)
    st.header("2️⃣ Transcripción")
    
    transcription_text = st.text_area(
        "Pega tu transcripción aquí:",
        height=150,
        placeholder="Ej: Esta es mi grabación de voz..."
    )
    
    # ============================================
    # PROCESAR CON IA
    # ============================================
    if transcription_text and claude_key:
        st.header("3️⃣ Procesamiento con IA")
        
        if st.button("🚀 Procesar con Claude"):
            with st.spinner("IA procesando..."):
                try:
                    import anthropic
                    
                    client = anthropic.Anthropic(api_key=claude_key)
                    
                    prompts = {
                        "📝 Solo transcribir": transcription_text,
                        "📋 Resumir": f"Resume en 3-5 puntos este texto:\n\n{transcription_text}",
                        "🏷️ Clasificar": f"Clasifica en categorías (Trabajo, Personal, Ideas, Urgente):\n\n{transcription_text}",
                        "✅ Extraer acciones": f"Extrae SOLO las acciones/tareas:\n\n{transcription_text}",
                        "🔍 Análisis completo": f"Analiza: resumen, temas, sentimiento, recomendaciones:\n\n{transcription_text}"
                    }
                    
                    prompt = prompts[action]
                    
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=1024,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    result = response.content[0].text
                    
                    st.success("✅ Procesado!")
                    st.markdown(result)
                    
                    # Descargar
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(
                        label="📥 Descargar resultado",
                        data=result,
                        file_name=f"resultado_{timestamp}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Limpiar
    if os.path.exists("temp_audio.wav"):
        os.remove("temp_audio.wav")

else:
    st.info("👆 Sube un archivo para empezar")

st.markdown("---")
st.markdown("Hecho por la IA Claude| Audio + IA ☁️")
