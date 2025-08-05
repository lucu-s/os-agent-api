# Módulo para la configuración de la base de datos de SQLAlchemy.
# Este archivo define el motor de la base de datos, la sesión local
# y la clase base para los modelos declarativos.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Es una buena práctica leer la URL de la base de datos de una variable de entorno.
# Usamos una URL por defecto para el desarrollo.
# Por ejemplo: DATABASE_URL = "postgresql://user:password@host:port/dbname"
DATABASE_URL = "sqlite:///./agent_data.db"

# Crea el motor de la base de datos.
# 'connect_args' es necesario para SQLite con FastAPI para manejar múltiples hilos.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Crea la clase de sesión local para las interacciones con la DB.
# 'autocommit' y 'autoflush' están configurados para ser gestionados manualmente.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea la clase base para los modelos declarativos.
# Todos los modelos de la base de datos (en models.py) heredarán de esta clase.
Base = declarative_base()
