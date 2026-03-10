# Usa una imagen oficial y ligera de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /code

# Copia los archivos de requerimientos primero (para aprovechar la cache de Docker)
COPY ./requirements.txt /code/requirements.txt

# Instala las dependencias sin cache local
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia el código fuente (la carpeta 'app') al contenedor
COPY ./app /code/app

# Variables de entorno por defecto
ENV PORT=8000
ENV HOST=0.0.0.0

# Expone el puerto donde se ejecutará FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
