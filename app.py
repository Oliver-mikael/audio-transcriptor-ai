import streamlit as st
from huggingface_hub import inference_client
import os
from datetime import datetime

# Configuración
st.set_page_config(page_title="Audio Transcriptor AI", layout="wide")

st.title("🎤 Transcriptor de Audio + IA")
st.markdown("Sube audio → Transcribe → Procesa con IA")

# ============================================
# SIDEBAR - Configuración
# ============================================
with st.sidebar:
    st.header("⚙️ Configuración")
    
    hf_token = st.text_input(
        "🔑 Token HuggingFace (gratis):",
        type="password",
        help="Obten en: https://huggingface.co/settings/tokens"
    )
    
    action = st.radio(
        "¿Qué quieres hacer con la transcripción?",
        ["📝 Solo transcribir",
         "📋 Resumir",
         "🏷️ Clasificar en categorías",
         "✅ Extraer acciones",
         "🔍 Análisis personalizado"]
    )

# ============================================
# MAIN - Upload Audio
# ============================================
st.header("1️⃣ Sube tu Audio")

uploaded_file = st.file_uploader(
    "Sube un archivo de audio (mp3, wav, m4a, ogg)",
    type=["mp3", "wav", "m4a", "ogg", "flac"]
)

if uploaded_file and hf_token:
    st.success("✅ Archivo cargado. Procesando...")
    
    # Guardar archivo temporalmente
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Transcribir con Whisper (HuggingFace)
    try:
        client = inference_client.InferenceClient(
            api_key=hf_token
        )
        
        with open("temp_audio.wav", "rb") as audio_file:
            transcription = client.automatic_speech_recognition(
                audio_file,
                model="openai/whisper-small"
            )
        
        transcription_text = transcription.get("text", "")
        
        st.success("✅ Transcripción completada!")
        
        # ============================================
        # TRANSCRIPCIÓN
        # ============================================
        st.header("2️⃣ Transcripción")
        st.text_area("Texto transcrito:", transcription_text, height=150)
        
        # ============================================
        # PROCESAR CON IA
        # ============================================
        st.header("3️⃣ Procesamiento con IA")
        
        if st.button("🚀 Procesar con IA"):
            with st.spinner("IA procesando..."):
                # Prompts según acción
                prompts = {
                    "📝 Solo transcribir": "Devuelve solo el texto transcrito sin cambios.",
                    "📋 Resumir": f"Resume en 3-5 puntos clave este texto:\n\n{transcription_text}",
                    "🏷️ Clasificar en categorías": f"Clasifica este texto en categorías (ej: Trabajo, Personal, Ideas, Urgente):\n\n{transcription_text}",
                    "✅ Extraer acciones": f"Extrae SOLO las acciones/tareas que se deben hacer de este texto:\n\n{transcription_text}",
                    "🔍 Análisis personalizado": f"Analiza profundamente este texto (resumen, temas, sentimiento, recomendaciones):\n\n{transcription_text}"
                }
                
                prompt = prompts[action]
                
                # Usar Claude API (necesita token)
                try:
                    import anthropic
                    client_claude = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
                    
                    response = client_claude.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=1024,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    result = response.content[0].text
                    st.success("✅ IA procesada!")
                    st.markdown(result)
                    
                    # Guardar resultado
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(
                        label="📥 Descargar resultado",
                        data=result,
                        file_name=f"resultado_{timestamp}.txt",
                        mime="text/plain"
                    )
                
                except:
                    st.warning("⚠️ Claude API no configurada. Solo transcripción disponible.")
        
        # Limpiar archivo temporal
        os.remove("temp_audio.wav")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

elif uploaded_file and not hf_token:
    st.warning("⚠️ Ingresa tu token de HuggingFace en la barra lateral")

else:
    st.info("👆 Sube un archivo de audio para empezar")

# Footer
st.markdown("---")
st.markdown("Hecho por Oliver | Transcripción + IA en la nube ☁️")
