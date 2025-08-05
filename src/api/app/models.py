# Módulo para los modelos de la base de datos SQLAlchemy.
# Estos modelos definen la estructura de las tablas de nuestra base de datos.

from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship

# Importamos la clase Base de nuestro archivo 'database.py'.
# Esta es la única Base que usaremos para todos los modelos del proyecto.
from .database import Base

class AgentDataDB(Base):
    """
    Este modelo representa la tabla 'agent_data', donde guardamos la información
    principal que nos envía cada agente. Es como el "expediente" de cada servidor.
    """
    __tablename__ = "agent_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Columna indexada para encontrar a los agentes rápidamente por su IP.
    client_ip = Column(String, nullable=False, index=True)
    
    # Aquí almacenamos los datos del sistema operativo y el nombre del host.
    hostname = Column(String, nullable=True)
    os_name = Column(String, nullable=False)
    os_version = Column(String, nullable=False)
    
    # Guardamos la información del procesador en un formato JSON.
    cpu_info = Column(JSON, nullable=False)
    
    # Definimos las relaciones con las otras tablas.
    # Con 'cascade', si borramos un agente, sus procesos y usuarios también se borran.
    processes = relationship("ProcessInfoDB", back_populates="agent_data", cascade="all, delete-orphan")
    users = relationship("UserSessionDB", back_populates="agent_data", cascade="all, delete-orphan")

class ProcessInfoDB(Base):
    """
    Este modelo representa la tabla 'process_info', donde guardamos
    la lista de procesos que estaban corriendo en el agente.
    """
    __tablename__ = "process_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    # Se permite que el nombre de usuario sea nulo si no está disponible.
    username = Column(String, nullable=True)
    agent_data_id = Column(Integer, ForeignKey("agent_data.id"))
    agent_data = relationship("AgentDataDB", back_populates="processes")

class UserSessionDB(Base):
    """
    Este modelo representa la tabla 'user_session', donde registramos
    qué usuarios tienen una sesión abierta en el sistema.
    """
    __tablename__ = "user_session"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    terminal = Column(String, nullable=True)
    host = Column(String, nullable=True)
    # Usamos 'Float' para guardar el timestamp de inicio de sesión de forma numérica.
    started = Column(Float)
    agent_data_id = Column(Integer, ForeignKey("agent_data.id"))
    agent_data = relationship("AgentDataDB", back_populates="users")
