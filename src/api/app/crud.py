# Módulo: src/api/app/crud.py
# Contiene las funciones para la lógica de la base de datos (CRUD).

from sqlalchemy.orm import Session
from typing import Optional
from .models import AgentDataDB, ProcessInfoDB, UserSessionDB
from .schemas import AgentData

def create_agent_data(db: Session, agent_data: AgentData, client_ip: str):
    """
    Crea un nuevo registro de datos de agente en la base de datos,
    incluyendo información del sistema, procesos y usuarios.
    """
    # 1. Crea y guarda el registro principal del agente.
    db_agent = AgentDataDB(
        client_ip=client_ip,
        hostname=agent_data.os_info.hostname,
        os_name=agent_data.os_info.system,
        os_version=agent_data.os_info.version,
        cpu_info=agent_data.cpu_info.model_dump(),
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent) # Actualiza el objeto para obtener el ID de la base de datos

    # 2. Crea y asocia los registros de procesos.
    for proc in agent_data.processes:
        db_proc = ProcessInfoDB(
            pid=proc.pid,
            name=proc.name,
            username=proc.username,
            agent_data_id=db_agent.id
        )
        db.add(db_proc)

    # 3. Crea y asocia los registros de usuarios.
    for user in agent_data.users:
        db_user = UserSessionDB(
            name=user.name,
            terminal=user.terminal,
            host=user.host,
            started=user.started,
            agent_data_id=db_agent.id
        )
        db.add(db_user)

    # 4. Confirma los cambios de procesos y usuarios en la base de datos.
    db.commit()
    db.refresh(db_agent)

    return db_agent

def get_agent_data(db: Session, client_ip: Optional[str] = None, skip: int = 0, limit: int = 100):
    """
    Obtiene los registros de datos de los agentes, con opción de filtrar por IP.
    """
    query = db.query(AgentDataDB)
    if client_ip:
        query = query.filter(AgentDataDB.client_ip == client_ip)
    
    # Corrige la línea repetida y retorna los resultados de forma eficiente
    return query.offset(skip).limit(limit).all()

def get_agent_data_by_id(db: Session, data_id: int):
    """
    Obtiene un registro de agente específico por su ID.
    """
    return db.query(AgentDataDB).filter(AgentDataDB.id == data_id).first()
