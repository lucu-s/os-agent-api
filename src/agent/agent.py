# ---Agent.py---
# Este script es un agente ligero diseñado para recolectar información del sistema
# y enviarla a un endpoint de la API.
# Recolecta datos como el uso de CPU, procesos en ejecución, usuarios,
# e información del sistema operativo.

import psutil
import requests
import platform
import json
import socket
import os
from typing import Any, Dict, Optional, List

# --- Configuración del Agente ---
# URL del endpoint de la API para enviar datos.
# Reemplaza con la IP pública de tu instancia  puerto correcto.
API_ENDPOINT = "http://<Public_IPv4_Address>:5000/api/agent_data"

# Obtiene el token de la API de una variable de entorno.
API_TOKEN = os.getenv("API_TOKEN")

def collect_system_info() -> Dict[str, Any]:
    """
    Recopila toda la información del sistema y la estructura en un formato
    que coincide con el esquema AgentData de la API.
    """
    # 1. Información sobre el procesador
    cpu_freq = psutil.cpu_freq()
    cpu_info: Dict[str, Optional[float] | int] = {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency": cpu_freq.max if cpu_freq else None,
        "current_frequency": cpu_freq.current if cpu_freq else None,
        "cpu_usage_percent": psutil.cpu_percent(interval=1)
    }

    # 2. Listado de procesos en ejecución
    processes: List[Dict[str, Any]] = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # 3. Usuarios con una sesión abierta
    users: List[Dict[str, Any]] = []
    for user in psutil.users():
        users.append({
            "name": user.name,
            "terminal": user.terminal,
            "host": user.host,
            "started": user.started
        })

    # 4. Información del sistema operativo
    os_info: Dict[str, str] = {
        "system": platform.system(),
        "version": platform.version(),
        "hostname": socket.gethostname()
    }

    # 5. Estructura el payload final para que coincida con el schema de la API.
    system_info: Dict[str, Any] = {
        "cpu_info": cpu_info,
        # Nombres de los campos ajustados para coincidir con el schema de la API
        "processes": processes,
        "users": users,
        "os_info": os_info
    }
    return system_info

def send_data_to_api(data: Dict[str, Any]):
    """
    Envía los datos recolectados al endpoint de la API.
    """
    # Verifica que el token de la API esté definido.
    if not API_TOKEN:
        print("Error: API_TOKEN no está definida en las variables de entorno.")
        return
    
    # La clave de la API se envia con encabezado HTTP
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_TOKEN
    }

    try:
        # Pasa el diccionario de encabezados a la petición.
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        print("Datos enviados correctamente a la API.")
        print(f"Respuesta del servidor: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error al enviar datos: {e}")

if __name__ == "__main__":
    # Lógica principal del agente.
    print("Recolectando información del sistema...")
    info = collect_system_info()
    send_data_to_api(info)