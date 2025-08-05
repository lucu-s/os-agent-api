# Módulo: src/api/app/schemas.py
# Este archivo define los modelos de datos (esquemas) que usamos en la API.
# Pydantic nos ayuda a validar y serializar los datos de forma automática.

from pydantic import BaseModel, Field
from typing import List, Optional

# --- Primero, definimos los modelos para los objetos anidados ---
# El orden es importante: los modelos anidados deben estar primero.

class CPUInfo(BaseModel):
    """Esquema para la información detallada del procesador."""
    physical_cores: int
    total_cores: int
    max_frequency: Optional[float]
    current_frequency: Optional[float]
    cpu_usage_percent: float

class ProcessInfo(BaseModel):
    """Esquema para la información de un proceso en ejecución."""
    pid: int
    name: str
    username: Optional[str]

class UserSession(BaseModel):
    """Esquema para la información de una sesión de usuario."""
    name: str
    terminal: Optional[str]
    host: Optional[str]
    started: float

class OSInfo(BaseModel):
    """Esquema para la información del sistema operativo."""
    system: str
    version: str
    hostname: str

# --- Después, definimos los modelos principales de entrada y salida ---

class AgentData(BaseModel):
    """
    Este es el modelo de datos principal.
    Define la estructura que esperamos recibir del agente.
    """
    cpu_info: CPUInfo
    processes: List[ProcessInfo]
    users: List[UserSession]
    os_info: OSInfo

class AgentDataInDB(AgentData):
    """
    Este es el modelo de datos de salida de la API.
    Lo usamos para serializar los datos de la base de datos.
    Incluye campos adicionales como el ID y la IP.
    """
    id: int
    client_ip: str

    # Permite que el modelo se serialice desde un objeto de SQLAlchemy.
    class Config:
        orm_mode = True