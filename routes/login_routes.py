# routes/login_routes.py
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session
)
import bcrypt

login_bp = Blueprint("login", __name__)        # sin url_prefix

# ──────────────── estructuras en memoria ────────────────
usuarios = {}        # {username|correo: {"nombre":…, "hash":…, "email":…}}
instituciones = {}   # {correo_contacto: {...}}

# ───────────────────── /auth (página única) ─────────────────────
@login_bp.route("/auth")
def auth_page():
    return render_template(
        "statics/inicio_registro.html",
        header_file="index_header.html",
        footer_file="index_footer.html"
    )

# ───────────────── REGISTRO ─────────────────
@login_bp.route("/process_register/<tipo>", methods=["POST"])
def process_register(tipo):
    form = request.form

    # ───── REGISTRO DE USUARIO ─────
    if tipo == "usuario":
        if form["password"] != form["confirm_password"]:
            flash("Las contraseñas no coinciden.", "warning")
            return redirect(url_for("login.auth_page"))

        username = form["username"].lower().strip()
        correo   = form["email"].lower().strip()

        if username in usuarios or correo in usuarios:
            flash("Ese usuario o correo ya existe.", "warning")
            return redirect(url_for("login.auth_page"))

        hash_pw = bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt())
        nuevo = {
            "nombre": f"{form['first_name']} {form['last_name']}",
            "hash":   hash_pw,
            "email":  correo
        }
        # Acceso por usuario O por correo
        usuarios[username] = usuarios[correo] = nuevo
        flash("Usuario registrado. Inicia sesión.", "success")

    # ─── REGISTRO DE INSTITUCIÓN ───
    elif tipo == "institucion":
        if form["password"] != form["confirm_password"]:
            flash("Las contraseñas no coinciden.", "warning")
            return redirect(url_for("login.auth_page"))

        correo = form["contact_email"].lower().strip()
        if correo in instituciones:
            flash("Esa institución ya existe.", "warning")
            return redirect(url_for("login.auth_page"))

        hash_pw = bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt())
        instituciones[correo] = {
            "nombre":  form["institution_name"],
            "hash":    hash_pw,
            "phone":   form.get("phone", ""),
            "address": form.get("address", "")
        }
        flash("Institución registrada. Inicia sesión.", "success")

    else:
        flash("Tipo de registro no reconocido.", "danger")

    return redirect(url_for("login.auth_page"))

# ───────────────── LOGIN ─────────────────
@login_bp.route("/process_login/<tipo>", methods=["POST"])
def process_login(tipo):
    user_key = request.form["username"].lower().strip()
    pwd      = request.form["password"]

    if tipo == "usuario":
        user = usuarios.get(user_key)
        if user and bcrypt.checkpw(pwd.encode(), user["hash"]):
            session.update(role="usuario", name=user["nombre"], email=user["email"])
            flash(f"Bienvenido {user['nombre']}", "success")
            return redirect(url_for("main.index"))

    elif tipo == "institucion":
        inst = instituciones.get(user_key)
        if inst and bcrypt.checkpw(pwd.encode(), inst["hash"]):
            session.update(role="institucion", name=inst["nombre"], email=user_key)
            flash(f"Bienvenida institución {inst['nombre']}", "success")
            return redirect(url_for("main.index"))

    flash("Credenciales incorrectas.", "danger")
    return redirect(url_for("login.auth_page"))

# ───────────────── LOGOUT ─────────────────
@login_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("main.index"))
