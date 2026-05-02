from database import engine
from sqlmodel import SQLModel
import models

def create_db_and_tables():
    print("Conectando con la base de datos y creando tablas...")
    SQLModel.metadata.create_all(engine)
    print("¡Tablas creadas con éxito en pgAdmin!")

if __name__ == "__main__":
    create_db_and_tables()