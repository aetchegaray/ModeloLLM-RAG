📘 Asistente de Políticas Internas — Proyecto RAG con LLM + FastAPI + Streamlit
🧠 Descripción del Proyecto

Este proyecto consiste en desarrollar una aplicación tipo chatbot que permita consultar un reglamento de políticas internas utilizando lenguaje natural. La solución implementa una arquitectura RAG (Retrieval-Augmented Generation) basada en:

- Recuperación de contexto mediante FAISS y embeddings (e5-large-v2)
- Generación de respuestas con un modelo LLM (Mistral-7B-Instruct v0.2)
- Backend desarrollado en FastAPI
- Interfaz de usuario con Streamlit
- Dockerización completa para facilitar su ejecución y portabilidad.

🎯 Objetivos:
- Implementar un backend en FastAPI que reciba preguntas y genere respuestas en base a un reglamento interno.
- Construir una interfaz simple en Streamlit para consultas por parte del usuario.
- Procesar un documento PDF en texto estructurado para construir un índice vectorial con embeddings.
- Permitir una ejecución rápida y portable usando Docker.
- Permitir ejecución 100% offline al incluir modelos predescargados.


⚙️ Requisitos:
Tener Docker instalado y funcionando.
Tener Python 3.9+ instalado solo si se desea ejecutar build_index.py fuera del contenedor.
Tener cuenta en Hugging Face y ejecutar huggingface-cli login si se usa modo online.
Conexión a internet para descargar modelos desde Hugging Face la primera vez.

🚀 Instrucciones de Ejecución (modo Docker):

1. Clonar el repositorio en la instancia.
2. Construir el índice vectorial FAISS (una vez): python build_index.py Esto transforma el PDF en chunks, genera embeddings y guarda el índice FAISS.
3. Construir la imagen Docker: bash build_api.sh
(Internamente corre: docker build -t asistente-politicas .)
4. Ejecutar la aplicación en contenedor: bash run_docker.sh
(Internamente corre: docker run -p 8501:8501 -p 8000:8000 asistente-politicas)

Acceder desde el navegador:
Interfaz de usuario (Streamlit): http://localhost:8501
API (FastAPI): http://localhost:8000/docs

🌐 Modo Online: La aplicación puede funcionar descargando los modelos directamente desde Hugging Face si tiene conexión a internet y autenticación previa con huggingface-cli login.

LLM: mistralai/Mistral-7B-Instruct-v0.1
Embeddings: intfloat/e5-large-v2

📴 Modo Offline:
Si se desea ejecutar sin conexión, se pueden descargar previamente los modelos y colocarlos en:

models/
├── mistral-7b-instruct/
├── e5-large-v2/

El código detecta automáticamente si existen localmente y los carga en modo offline (local_files_only=True). Si el repositorio clonado no incluye los modelos, se puede ejecutar download_models.py previamente con conexión, o montar la carpeta models/ en la raíz del proyecto.

📌 Herramientas Utilizadas:
FastAPI
Streamlit
Hugging Face Transformers
LangChain
Sentence Transformers
FAISS
Docker