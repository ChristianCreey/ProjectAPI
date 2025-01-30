# ProjectAPI

## 1. Crear el Dockerfile

```dockerfile
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
```

---

## 2. Crear el archivo `docker-compose.yml`

```yaml
version: '3.8'

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
```

---

## 3. Construir la imagen

Ejecutar el siguiente comando:

```sh
docker build -t projectapi .
```

---

## 4. Ejecutar el contenedor

Puedes usar cualquiera de los siguientes comandos:

```sh
docker run -p 4000:4000 projectapi
```

O con la opción de eliminar el contenedor al detenerlo:

```sh
docker run -it --rm -p 4000:4000 projectapi
```

