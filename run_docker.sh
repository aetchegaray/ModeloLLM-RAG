echo "Iniciando contenedor..."

docker run \
  -p 8501:8501 \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/models:/app/models \
  asistente-politicas