import streamlit as st
import requests
import time

# Configurar la app
st.set_page_config(page_title="Asistente de Políticas Internas", layout="wide")

# Encabezado principal
st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>📘 Asistente de Políticas Internas</h1>
    <p style='text-align: center; font-size: 18px;'>
        Consultá el reglamento interno de la empresa con ayuda de un modelo de lenguaje.
    </p>
""", unsafe_allow_html=True)

# API backend
API_URL = "http://localhost:8000/query"

# Input de usuario
query = st.text_input("📝 Ingresá tu consulta sobre el reglamento interno:",
                      placeholder="Ej: ¿Cuántos días de licencia tengo por maternidad?",
                      key="consulta_input")

# Botón para consultar
if st.button("🔍 Consultar"):
    with st.spinner("Buscando en el reglamento..."):
        start = time.perf_counter()
        try:
            response = requests.post(API_URL, json={"question": query})
            data = response.json()
            respuesta = data.get("answer", "No se pudo generar respuesta.")
            tiempo = data.get("response_time", "-")
            fragmentos = data.get("context_docs", [])
            fallback = data.get("fallback", False)
        except Exception as e:
            respuesta = f"❌ Error al consultar la API: {e}"
            tiempo = "-"
            fragmentos = []
            fallback = False

    # Mostrar respuesta generada
    st.markdown(f"""
    <div style="background-color: #e8f0fe; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
        <h4 style="color: #1f77b4;">✅ Respuesta:</h4>
        <p style="font-size: 16px;">{respuesta}</p>
        <p style="font-size: 14px; color: gray;">⏱️ Tiempo de respuesta: {tiempo}</p>
    </div>
    """, unsafe_allow_html=True)

    if fallback:
        st.warning("⚠️ La respuesta fue tomada directamente del reglamento, ya que el modelo no pudo generar una respuesta.")

    # Mostrar fragmentos utilizados
    if fragmentos:
        with st.expander("📄 Documentos utilizados para responder"):
            for frag in fragmentos:
                st.markdown(f"""
                *{frag.get("articulo", "")}*  
                *Título:* {frag.get("titulo", "")}  
                *Capítulo:* {frag.get("capitulo", "")}  
                {"*Subcapítulo:* " + frag.get("subcapitulo", "") + " - " + frag.get("subtitulo", "") if frag.get("subcapitulo") else ""}
                
                Fragmento utilizado (recortado):
                > {frag.get("contenido", "")[:500]}...
                ---
                """)

# Sidebar con info y ejemplos
with st.sidebar:
    st.markdown("### ℹ️ Información")
    st.markdown("""
        - *Backend:* FastAPI + LangChain  
        - *Frontend:* Streamlit  
        - *Embeddings:* intfloat/e5-large-v2  
        - *Vector DB:* FAISS  
        - *LLM:* google/flan-t5-large
    """)
    st.markdown("---")
    st.markdown("### 🧠 Ejemplos de consulta")
    st.markdown("""
        - ¿Qué hago ante una situación de acoso laboral?
        - ¿Cuál es la política sobre diversidad?
    """)