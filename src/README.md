# Sentinel OS Agent API

## Descripción

Este proyecto implementa una API en **FastAPI** para recibir, almacenar y consultar información de agentes que recopilan datos del sistema operativo. El agente envía información sobre el procesador, procesos en ejecución, usuarios con sesión abierta y detalles del sistema operativo. Los datos se almacenan en una base de datos **SQLite** utilizando **SQLAlchemy**.

## Estructura del Proyecto
os-agent/
├── src/
│   ├── agent/agent.py           # Script del agente para recopilar y enviar datos
│   └── api/
│       ├── app/
│       │   ├── main.py          # Endpoints de la API y orquestador principal
│       │   ├── database.py      # Configuración de SQLAlchemy y motor de la DB
│       │   ├── models.py        # Modelos de la base de datos (tablas)
│       │   ├── schemas.py       # Modelos Pydantic para validación y serialización
│       │   └── crud.py          # Lógica de interacción con la base de datos (CRUD)
│       ├── requirements.txt     # Dependencias de la API
│       └── Dockerfile           # Imagen Docker para la API

## Instalación y Despliegue

### Requisitos

* **Python 3.11**
* **Docker** (recomendado para el despliegue)

### Instalación manual

1.  Clona el repositorio.
2.  Instala las dependencias de la API:
    ```bash
    cd src/api
    pip install -r requirements.txt
    ```
3.  La base de datos se creará automáticamente al ejecutar la API.

### Despliegue con Docker (Método recomendado)

La forma más sencilla y segura de desplegar la API es usando Docker.

1.  **Construye la imagen de Docker** en el directorio `src/api`:
    ```bash
    docker build -t sentinel-api .
    ```
2.  **Ejecuta el contenedor**, pasando el token de autenticación como variable de entorno y montando un volumen para persistir la base de datos:
    ```bash
    docker run -d -p 5000:5000 \
    -e API_TOKEN="tu_clave_secreta" \
    --name sentinel-api \
    -v $(pwd):/app \
    sentinel-api
    ```
    * `-e API_TOKEN="tu_clave_secreta"`: Pasa la clave de autenticación.
    * `-v $(pwd):/app`: Monta el directorio actual del host en el contenedor para que el archivo `agent_data.db` persista.

## Uso

### 1. Ejecutar el Agente

El agente (`src/agent/agent.py`) debe ejecutarse en el servidor que quieres monitorear.

1.  **Configura la URL del endpoint** en el archivo `agent.py` para que apunte a la IP pública server
2.  **Configura el token de la API** como una variable de entorno en la terminal:
    ```bash
    export API_TOKEN="tu_clave_secreta"
    ```
3.  **Ejecuta el agente**:
    ```bash
    python src/agent/agent.py
    ```

### 2. Endpoints de la API

* **POST /api/agent_data** **Descripción:** Recibe datos del agente en formato JSON y los almacena.
    **Autenticación:** Requiere la clave de la API en el parámetro de consulta `?api-key=`.

    Ejemplo de comando `curl` (para simular al agente):
    ```bash
    curl -X POST \
    -H "Content-Type: application/json" \
    -d '{ "cpu_info": { "physical_cores": 4, "total_cores": 8, "max_frequency": 3500.0, "current_frequency": 3200.0, "cpu_usage_percent": 12.5 }, "processes": [], "users": [], "os_info": { "system": "Linux", "version": "5.15.0-75-generic", "hostname": "mi-servidor" } }' \
    "http://<IP_API>:5000/api/agent_data?api-key=tu_clave_secreta"
    ```

* **GET /api/agent_data** **Descripción:** Consulta los datos almacenados en la base de datos.
    **Filtro:** Permite filtrar por la IP del cliente con el parámetro de consulta `?client_ip=`.
    **Autenticación:** Este endpoint es público y no requiere autenticación para la consulta.

    Ejemplo de comando `curl`:
    ```bash
    curl "http://<IP_API>:5000/api/agent_data?client_ip=<IP_AGENT>"
    ```

## Licencia

Consulta el archivo `LICENSE` para los detalles de la licencia.

## Autores

Consulta el archivo `AUTHORS` para la lista de contribuyentes.