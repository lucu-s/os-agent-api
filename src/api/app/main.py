# Módulo principal de la aplicación FastAPI.
# Este archivo define los endpoints de la API y orquesta la interacción
# entre los demás módulos (modelos, esquemas y lógica de la base de datos).

# Importaciones necesarias de tu proyecto.
from fastapi import FastAPI, Request, Query, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os

# Importa los objetos de la base de datos
from .database import SessionLocal, engine, Base

# Importa TODOS los modelos de la base de datos para que las tablas se creen
from .models import AgentDataDB, ProcessInfoDB, UserSessionDB

# Importa las clases y funciones de tus otros módulos de forma explícita
from .schemas import AgentData, AgentDataInDB
from .crud import create_agent_data, get_agent_data

# Aseguramos que la base de datos se inicialice y cree las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Relevamiento de Servidores",
    description="API que recibe y consulta información de agentes en servidores."
)

# Dependencia para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/agent_data", status_code=status.HTTP_201_CREATED)
async def receive_data(
    agent_data: AgentData, 
    request: Request, 
    db: Session = Depends(get_db)
):
    """
    Recibe la información de un agente y la almacena en la base de datos.
    """
    client_ip = request.client.host
    db_agent = create_agent_data(db, agent_data, client_ip)
    
    return {
        "message": "Data received", 
        "client_ip": client_ip, 
        "id": db_agent.id
    }

@app.get("/api/agent_data", response_model=List[AgentDataInDB])
def read_agent_data(
    client_ip: Optional[str] = Query(None, description="Filtrar por IP del cliente"), 
    db: Session = Depends(get_db)
):
    """
    Consulta la información de los agentes, opcionalmente filtrando por IP.
    """
    results = get_agent_data(db, client_ip)

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron datos para la IP especificada"
        )
    
    # FastAPI con response_model se encarga de la serialización,
    # por lo que no es necesario el bucle manual.
    return results