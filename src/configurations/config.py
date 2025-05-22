"""
Configuración central de Cyberhole_ong
──────────────────────────────────────
• Carga las variables del archivo `.env`.
• Define clases de configuración para Flask.
• Expone helpers para conectarse a MySQL.
"""

import os
from dotenv import load_dotenv
import pymysql

# ─────────────── .env ────────────────
load_dotenv()                                     # lee las claves DB_* y SECRET_KEY

# ───────────  BASE CONFIG  ───────────
class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "cambia-esto").strip()
    SQLALCHEMY_TRACK_MODIFICATIONS = False        # desactiva warning de Flask-SQLAlchemy

    DB_HOST     = os.getenv("DB_HOST", "").strip()
    DB_PORT     = int(os.getenv("DB_PORT", 3306))
    DB_NAME     = os.getenv("DB_NAME", "").strip()
    DB_USER     = os.getenv("DB_USER", "").strip()
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# ───────────  ENTORNOS  ──────────────
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASSWORD}"
        f"@{BaseConfig.DB_HOST}:{BaseConfig.DB_PORT}/{BaseConfig.DB_NAME}"
    )

class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{BaseConfig.DB_USER}:{BaseConfig.DB_PASSWORD}"
        f"@{BaseConfig.DB_HOST}:{BaseConfig.DB_PORT}/{BaseConfig.DB_NAME}"
    )

# Mapa que `app.py` utilizará
config = {
    "development": DevelopmentConfig,
    "testing":     TestingConfig,
    "production":  ProductionConfig,
}

# ─────────  HELPERS BD  ──────────────
def get_db_params() -> dict:
    """Devuelve kwargs listos para `pymysql.connect(**params)`."""
    return {
        "host":        BaseConfig.DB_HOST,
        "port":        BaseConfig.DB_PORT,
        "user":        BaseConfig.DB_USER,
        "password":    BaseConfig.DB_PASSWORD,
        "db":          BaseConfig.DB_NAME,
        "charset":     "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,
    }

def test_db_connection() -> tuple[bool, str]:
    """Prueba de conexión rápida (dev)."""
    params = get_db_params().copy()
    params.pop("cursorclass")
    try:
        conn = pymysql.connect(**params, connect_timeout=3)
        conn.close()
        return True, "Conexión exitosa"
    except pymysql.MySQLError as exc:
        return False, str(exc)

# ───────── TEST MANUAL opcional ──────
if __name__ == "__main__":
    ok, msg = test_db_connection()
    print("DB_HOST:", BaseConfig.DB_HOST)
    print("DB_NAME:", BaseConfig.DB_NAME)
    print("Estado conexión:", msg)
