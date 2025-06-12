# Imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY requirements.txt requirements.txt
COPY bot.py bot.py

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto para Railway
EXPOSE 5000

# Comando para iniciar la app
CMD ["python", "bot.py"]
