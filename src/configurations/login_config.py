# ────────────────────────────────────────────────────────────────
#  src/routes/login_routes.py        (versión estable 21-may-2025)
# ────────────────────────────────────────────────────────────────
from __future__ import annotations
from datetime import datetime

from flask import (
    Blueprint, render_template, request,
    redirect, url_for
)
from flask_login import (
    login_user, logout_user, login_required,
    UserMixin
)
import bcrypt
import pymysql
from dotenv import load_dotenv

from extensions            import login_manager
from configurations.config import get_db_params

load_dotenv()
login_bp = Blueprint("login", __name__, url_prefix="")

# ════════════════════════════════════════════════════════════════
#  1.  Página única LogIn / Registro
# ════════════════════════════════════════════════════════════════
@login_bp.route("/auth")
def login_page():
    return render_template(
        "aut_statics/inicio_registro.html",
        header_file="index_header.html",
        footer_file="index_footer.html"
    )

# ════════════════════════════════════════════════════════════════
#  2.  Conexión MySQL helper
# ════════════════════════════════════════════════════════════════
def get_conn() -> pymysql.connections.Connection:
    """Devuelve conexión pymysql con los parámetros de .env"""
    return pymysql.connect(**get_db_params())

# ════════════════════════════════════════════════════════════════
#  3.  Modelo para Flask-Login
# ════════════════════════════════════════════════════════════════
class User(UserMixin):
    def __init__(self, id_: int, email: str, tipo: str):
        self.id    = id_
        self.email = email
        self.tipo  = tipo          # 'usuarios' | 'instituciones'

# Carga de usuario desde ID (sesiones)
@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    qry = """
        SELECT id_user       AS id,
               user_name     AS email,
               'usuarios'    AS tipo
          FROM usuarios
         WHERE id_user = %s

        UNION ALL

        SELECT id            AS id,
               email_contacto AS email,
               'instituciones' AS tipo
          FROM instituciones
         WHERE id = %s;
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(qry, (user_id, user_id))
        row = cur.fetchone()
    return User(**row) if row else None

# ════════════════════════════════════════════════════════════════
#  4.  LOGIN
# ════════════════════════════════════════════════════════════════
@login_bp.route("/process_login/<tipo>", methods=["POST"])
def process_login(tipo: str):
    """
    Recibe el tipo ('usuarios' | 'instituciones') y verifica credenciales.
    Redirige a /status/success o /status/error.
    """
    try:
        if tipo == "usuarios":
            username = request.form.get("user_name", "").strip()
            pwd      = request.form.get("password", "").encode()

            with get_conn() as conn, conn.cursor() as cur:
                cur.execute("""
                    SELECT id_user AS id, user_name AS email, contrasena
                      FROM usuarios
                     WHERE user_name = %s
                     LIMIT 1
                """, (username,))
                row = cur.fetchone()

        elif tipo == "instituciones":
            email = request.form.get("email_contacto", "").strip()
            pwd   = request.form.get("password", "").encode()

            with get_conn() as conn, conn.cursor() as cur:
                cur.execute("""
                    SELECT id, email_contacto AS email, contrasena
                      FROM instituciones
                     WHERE email_contacto = %s
                     LIMIT 1
                """, (email,))
                row = cur.fetchone()

        else:
            return redirect(url_for("login.status", tipo="error"))

        if not row or not bcrypt.checkpw(pwd, row["contrasena"].encode()):
            return redirect(url_for("login.status", tipo="error"))

        login_user(User(row["id"], row["email"], tipo))
        return redirect(url_for("login.status", tipo="success"))

    except Exception as exc:
        print("ERROR LOGIN:", repr(exc))
        return redirect(url_for("login.status", tipo="error"))

# ════════════════════════════════════════════════════════════════
#  5.  REGISTRO
# ════════════════════════════════════════════════════════════════
@login_bp.route("/process_register/<tipo>", methods=["POST"])
def process_register(tipo: str):
    """
    Inserta un nuevo registro en usuarios o instituciones.
    Valida campos obligatorios y contraseñas.
    """
    pwd  = request.form.get("password", "").encode()
    cpwd = request.form.get("confirm_password", "").encode()
    if not pwd or pwd != cpwd:
        return redirect(url_for("login.status", tipo="error"))

    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt()).decode()

    try:
        with get_conn() as conn, conn.cursor() as cur:

            # ─────────────────────────  USUARIOS  ─────────────────────────
            if tipo == "usuarios":
                nombres   = request.form.get("nombres", "").strip()
                paterno   = request.form.get("apellido_paterno", "").strip()
                materno   = request.form.get("apellido_materno", "").strip()
                user_nm   = request.form.get("user_name", "").strip()

                # Mapear género (‘M’, ‘F’, ‘O’) → ajusta si tu ENUM usa texto
                genero_map = {"masculino": "M", "femenino": "F", "otro": "O"}
                genero_val = genero_map.get(request.form.get("genero", "").lower())

                # Fecha nacimiento a DATE o NULL
                fecha_txt  = request.form.get("fecha_nacimiento") or None
                try:
                    fecha_val = datetime.strptime(fecha_txt, "%Y-%m-%d").date() if fecha_txt else None
                except ValueError:
                    fecha_val = None

                if not all([nombres, paterno, user_nm, genero_val]):
                    return redirect(url_for("login.status", tipo="error"))

                # Evitar duplicado user_name
                cur.execute("SELECT 1 FROM usuarios WHERE user_name=%s", (user_nm,))
                if cur.fetchone():
                    return redirect(url_for("login.status", tipo="error"))

                cur.execute("""
                    INSERT INTO usuarios (
                        nombres, apellido_paterno, apellido_materno,
                        user_name, contrasena,
                        fecha_nacimiento, c_p, genero
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    nombres, paterno, materno or None,
                    user_nm, hashed,
                    fecha_val, request.form.get("c_p") or None, genero_val
                ))

            # ────────────────────────  INSTITUCIONES  ──────────────────────
            elif tipo == "instituciones":
                nombre = request.form.get("nombre_comercial", "").strip()
                email  = request.form.get("email_contacto", "").strip()

                if not nombre or not email:
                    return redirect(url_for("login.status", tipo="error"))

                cur.execute("SELECT 1 FROM instituciones WHERE email_contacto=%s", (email,))
                if cur.fetchone():
                    return redirect(url_for("login.status", tipo="error"))

                cur.execute("""
                    INSERT INTO instituciones (
                        nombre_comercial, razon_social,
                        email_contacto, telefono_contacto, contrasena
                    ) VALUES (%s,%s,%s,%s,%s)
                """, (
                    nombre,
                    request.form.get("razon_social", "").strip() or None,
                    email,
                    request.form.get("telefono_contacto", "").strip() or None,
                    hashed
                ))

            else:
                return redirect(url_for("login.status", tipo="error"))

            conn.commit()
            return redirect(url_for("login.status", tipo="success"))

    except pymysql.IntegrityError as ie:
        print("IntegrityError registro:", ie)
        return redirect(url_for("login.status", tipo="error"))
    except Exception as exc:
        print("ERROR REGISTRO:", repr(exc))
        return redirect(url_for("login.status", tipo="error"))

# ════════════════════════════════════════════════════════════════
#  6.  STATUS (consola + respuesta mínima)
# ════════════════════════════════════════════════════════════════
@login_bp.route("/status/<tipo>")
def status(tipo: str):
    mensajes = {
        "success": "✅ Operación exitosa",
        "error":   "❌ Ocurrió un error durante el proceso",
        "info":    "ℹ️ Sesión cerrada correctamente"
    }
    print(f"[STATUS]: {mensajes.get(tipo,'⚠️ Desconocido')}")
    return mensajes.get(tipo, "Desconocido")

# ════════════════════════════════════════════════════════════════
#  7.  LOGOUT
# ════════════════════════════════════════════════════════════════
@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.status", tipo="info"))
