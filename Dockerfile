FROM python:3.11-alpine
LABEL authors="Nicolás Suárez"

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar las dependencias del sistema necesarias para compilar extensiones (bcrypt/cryptography)
RUN apk add --no-cache gcc musl-dev libffi-dev rust cargo openssl-dev

# Copiar y instalar dependencias Python primero (mejor caché)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto 5000
EXPOSE 5000

# Ejecutar la aplicación
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]


#docker run --name some-mysql \
#  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
#  -e MYSQL_DATABASE=mydatabase \
#  -e MYSQL_USER=myuser \
#  -e MYSQL_PASSWORD=myuser-pw \
#  -p 3306:3306 \
#  -d mysql:latest
