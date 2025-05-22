📘 Asistente de Políticas Internas — Proyecto RAG con LLM + FastAPI + Streamlit + Docker
🧠 Descripción del Proyecto

Este proyecto consiste en desarrollar una aplicación tipo chatbot que permita consultar un reglamento de políticas internas utilizando lenguaje natural. La solución implementa una arquitectura RAG (Retrieval-Augmented Generation) basada en:

- Recuperación de contexto mediante un índice FAISS, utiizando embeddings generados con el modelo e5-large-v2.
- Generación de respuestas con un modelo LLM (google/flan-t5-large), operando sobre el contexto recuperado.
- Backend desarrollado en FastAPI.
- Interfaz de usuario desarrollada en Streamlit.
- Contenerización en Docker para facilitar su ejecución y portabilidad.

🎯 Objetivos:
- Implementar un backend en FastAPI que reciba preguntas y genere respuestas en base a un reglamento interno.
- Construir una interfaz simple en Streamlit para consultas por parte del usuario.
- Procesar un documento PDF en texto estructurado para construir un índice vectorial con embeddings.
- Permitir una ejecución rápida y portable usando Docker.

⚙️ Requisitos:
Tener Docker instalado y funcionando.
Tener Python 3.9+ instalado solo si se desea ejecutar build_index.py fuera del contenedor.
Tener cuenta en Hugging Face y ejecutar huggingface-cli login si se usa modo online.
Conexión a internet para descargar modelos desde Hugging Face la primera vez.

Componentes del Proyecto:
    - setup_api.sh: Script de preparación inicial del entorno.
    - app: contiene los módulos del backend (parser del PDF, construcción del índice FAISS y lógica del RAG)
    - Dockerfile: define el entorno contenerizado que ejecuta tanto la API como la interfaz de usuario.
    - build_index.py: Script para procesar el PDF de políticas internas, generar los embeddings y construir el índice vectorial FAISS.
    - rag_chain.py: Define la cadena de recuperación y generación (RAG) utilizando LangChain y el modelo LLM.
    - main.py: Backend con FastAPI que expone la API para recibir preguntas y devolver respuestas generadas.
    - streamlit_app.py: Script de Streamlit que permite interactuar con el asistente a través de una interfaz web.
    - build_api.sh: Script para construir la imagen Docker.
    - run_docker.sh: Script para ejecutar el contenedor Docker exponiendo los puertos.
    - requirements.txt: listado de librerías y dependencias necesarias para la ejecución del proyecto.

🚀 Instrucciones de Ejecución:

1. Clonar el repositorio en la instancia.
2. Ejecutar setup_api.sh para crear entorno virtual y descargar los requirements.
3. Construir el índice vectorial FAISS (una única vez si no hay modificaciones en el documento 'politicas_internas.pdf'): python build_index.py 
4. Construir la imagen Docker: bash build_api.sh
5. Ejecutar la aplicación en contenedor: bash run_docker.sh

Acceder desde el navegador:
Interfaz de usuario (Streamlit): http://localhost:8501
API (FastAPI): http://localhost:8000/docs


📌 Herramientas Utilizadas:
FastAPI
Streamlit
Hugging Face Transformers
LangChain
Sentence Transformers
FAISS
Docker
Uvicorn
pdfminer.six