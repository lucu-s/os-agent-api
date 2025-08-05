# Usa una imagen base oficial de Python 3.11 en su versión ligera.
FROM python:3.11-slim

# Define un directorio de trabajo para tu aplicación dentro del contenedor.
WORKDIR /app

# Copia primero el archivo de dependencias para optimizar el cacheo de capas.
COPY requirements.txt .

# Instala las dependencias de la aplicación.
# '--no-cache-dir' reduce el tamaño final de la imagen.
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente de tu proyecto.
COPY . .

# Expone el puerto en el que la API escuchará. Esto es para documentación.
EXPOSE 5000

# Define el comando por defecto para ejecutar la aplicación con uvicorn.
# 'app.main:app' se refiere al objeto 'app' en el archivo 'main.py' dentro del paquete 'app'.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]