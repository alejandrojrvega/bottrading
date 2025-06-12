# Usa una imagen oficial de Python
FROM python:3.11-slim

# Crea y establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt requirements.txt
COPY bot.py bot.py
COPY .env .env

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que utiliza Flask
EXPOSE 5000

# Comando para ejecutar el servidor Flask
CMD ["python", "bot.py"]
