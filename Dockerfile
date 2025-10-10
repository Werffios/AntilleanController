FROM python:3.11-alpine
LABEL authors="Nicolás Suárez"

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación
COPY . .

# Instalar las dependencias del sistema
RUN apk add --no-cache gcc musl-dev libffi-dev rust cargo

# Copy requirements.txt first
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5000
EXPOSE 5000

# Ejecutar la aplicación
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]

# Añadir un healthcheck para verificar que la aplicación está funcionando
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl --fail http://127.0.0.1:5000/health || exit 1


#docker run --name some-mysql \
#  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
#  -e MYSQL_DATABASE=mydatabase \
#  -e MYSQL_USER=myuser \
#  -e MYSQL_PASSWORD=myuser-pw \
#  -p 3306:3306 \
#  -d mysql:latest

