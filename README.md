# ProjectAPI


1. Crear el Dockerfile

    # Usar una imagen base de Python
    FROM python:3.10-slim

    # Establecer el directorio de trabajo
    WORKDIR /app

    # Copiar los archivos del proyecto al contenedor
    COPY . .

    # Instalar dependencias
    RUN pip install --no-cache-dir -r requirements.txt

    # Exponer el puerto de la API
    EXPOSE 4000

    # Comando para ejecutar la aplicación
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]

2. Crear el docker-compose.yml

    services:
        app:
            build:
                context: .
            ports:
                - "4000:4000"
            volumes:
                - .:/app
            environment:
                - ENV=production

3. construir la imagen

    docker build -t projectapi .

4. Ejecutar el contenedor (cualquir comando de los 2 funciona)

    docker run -p 4000:4000 projectapi
    docker run -it --rm -p 4000:4000 projectapi
