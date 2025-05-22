#!/bin/bash
echo "Iniciando backend FastAPI en segundo plano..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Esperar a que el backend arranque
sleep 2

echo "Iniciando frontend Streamlit..."
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0