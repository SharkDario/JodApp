# Usa una imagen base de Python
FROM python:3.11

# Instala las dependencias necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos a /app
COPY requirements.txt /app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del proyecto a /app
COPY . /app/

# Expone el puerto que utiliza Django (por defecto 8000)
EXPOSE 8000

# Comando para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
