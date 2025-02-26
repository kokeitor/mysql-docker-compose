import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from typing import Optional
from pathlib import Path

# Cargar variables desde el archivo .env si existe
load_dotenv()


class DatabaseManager:
    """
    Clase para gestionar la conexión y ejecución de scripts SQL con SQLAlchemy.

    Permite conectarse a bases de datos como MySQL, PostgreSQL, SQLite y Oracle usando SQLAlchemy.
    También puede ejecutar múltiples archivos SQL desde un directorio.

    Args:
        db_url (str): URL de conexión en formato SQLAlchemy.
        sql_directory (Optional[str]): Ruta a un directorio con múltiples archivos .sql a ejecutar.
    """

    def __init__(self, db_url: str, sql_directory: Optional[str] = None):
        """
        Inicializa el gestor de base de datos.

        Args:
            db_url (str): URL de conexión en formato SQLAlchemy.
            sql_directory (Optional[str]): Ruta de un directorio con archivos .sql (opcional).
        """
        self.db_url = db_url
        self.sql_directory = Path(sql_directory)
        self.engine = create_engine(self.db_url, echo=False, future=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def execute_script(self, script_path: str):
        """
        Ejecuta un archivo SQL en la base de datos.

        Args:
            script_path (str): Ruta del archivo SQL a ejecutar.

        Raises:
            Exception: Si ocurre un error en la ejecución del script.
        """
        try:
            with open(script_path, "r", encoding="utf-8") as sql_file:
                sql_script = sql_file.read()

            with self.engine.connect() as connection:
                for statement in sql_script.split(";"):
                    if statement.strip():
                        connection.execute(text(statement))
                connection.commit()

            print(f"[INFO] Script ejecutado con éxito: {script_path}")

        except Exception as e:
            print(f"[ERROR] Error al ejecutar el script {script_path}: {e}")

    def execute_scripts_from_directory(self):
        """
        Itera sobre todos los archivos SQL en el directorio especificado y los ejecuta en orden.

        Raises:
            FileNotFoundError: Si el directorio no existe o no contiene archivos SQL.
        """
        if not self.sql_directory:
            print("[ERROR] No se especificó un directorio de scripts SQL.")
            return

        if not os.path.exists(self.sql_directory) or not os.path.isdir(self.sql_directory):
            raise FileNotFoundError(
                f"[ERROR] El directorio {self.sql_directory} no existe.")

        sql_files = sorted([f for f in os.listdir(
            self.sql_directory) if f.endswith(".sql")])

        if not sql_files:
            print(
                f"[ERROR] No se encontraron archivos SQL en {self.sql_directory}.")
            return

        print(
            f"[INFO] Se encontraron {len(sql_files)} archivos SQL en {self.sql_directory}. Ejecutándolos...")

        for sql_file in sql_files:
            script_path = os.path.join(self.sql_directory, sql_file)
            self.execute_script(script_path)

        print("[INFO] Todos los scripts SQL han sido ejecutados correctamente.")

    def disconnect(self):
        """Cierra la conexión con la base de datos."""
        self.session.close()
        print("[INFO] Conexión cerrada.")


# ============================
# USO DEL CÓDIGO
# ============================

if __name__ == "__main__":
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

    # Inicializar el gestor de base de datos con los valores del .env
    db_manager = DatabaseManager(DATABASE_URL, SQL_DIRECTORY)

    try:
        # Ejecuta todos los scripts en el directorio
        db_manager.execute_scripts_from_directory()
    finally:
        db_manager.disconnect()
