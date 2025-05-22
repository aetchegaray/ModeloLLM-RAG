# Imagen base ligera con Python
FROM python:3.9-slim
# Establecer el directorio de trabajo
WORKDIR /app
#Evitar interacción manual en la construcción del Docker
ENV DEBIAN_FRONTEND=noninteractive
# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
# Copiar archivos de requisitos e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copiar todo el código fuente al contenedor
COPY . /app
# Dar permisos de ejecución al script de arranque
RUN chmod +x /app/run_all.sh
# Exponer puertos usados por Streamlit y FastAPI
EXPOSE 8501 8000
# Comando de inicio (ejecuta backend + frontend)
ENTRYPOINT ["/app/run_all.sh"]