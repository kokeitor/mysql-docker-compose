from fastapi import FastAPI, Depends
import pathlib
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean
import datetime


load_dotenv()
# Leer configuración desde variables de entorno o .env
DB_TYPE = os.getenv("DB_TYPE", "mysql").lower()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "test_db")
SQL_DIRECTORY = os.getenv("SQL_DIRECTORY", "./app/factiva_data/sql")

print(SQL_DIRECTORY)
print(DB_TYPE)
print(DB_HOST)
print(DB_PORT)
print(DB_USER)
print(DB_PASSWORD)

# Construir la URL de conexión según el tipo de base de datos
if DB_TYPE == "mysql":
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DB_TYPE == "postgresql":
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DB_TYPE == "sqlite":
    DATABASE_URL = f"sqlite:///{DB_NAME}.db"
elif DB_TYPE == "oracle":
    DATABASE_URL = f"oracle+cx_oracle://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?service_name={DB_NAME}"
else:
    raise ValueError(
        f"[ERROR] Tipo de base de datos '{DB_TYPE}' no soportado.")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False)


BASE = declarative_base()


class Booking(BASE):
    __tablename__ = "reservas"

    id = Column(Integer, autoincrement=True, unique=True,
                nullable=False, primary_key=True)
    client_name = Column(String(50), nullable=False)
    timestamp = Column(String, nullable=False,
                       default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __repr__(self):
        return f"Clients(id={self.id}, name='{self.name}', timestamp='{self.timestamp}')"

    def to_dict(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "timestamp": self.timestamp
        }


BASE.metadata.create_all(engine)


class requestModel(BaseModel):
    client_name: str


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/')
def hello_world(request: requestModel,  db: Session = Depends(get_db)):

    booking = Booking(client_name=request.client_name)
    print(
        f"Before insert >> Searching for name {booking.client_name} in bbdd >> {db.query(Booking).filter(Booking.client_name == request.client_name).first()})")
    db.add(booking)
    db.commit()
    db.refresh(booking)
    print(
        f"After insert >> Searching for name {Booking.client_name} in bbdd >> {db.query(Booking).filter(Booking.client_name == request.client_name).first()})")

    return {'response': f'Created booking >> {booking.to_dict()}'}
