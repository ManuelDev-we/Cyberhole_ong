# ───────────────────────────────────────────────────────────────────
#  src/app.py
#  Arranque principal de *Cyberhole_ong*
#  • Carga configuración desde configurations/config.py (.env)
#  • Inicializa extensiones declaradas en src/extensions.py
#  • Registra TODOS los blueprints disponibles
#  • Añade manejadores 401 / 404
# ───────────────────────────────────────────────────────────────────

import os
from flask import Flask, redirect, url_for
from configurations.config import config as CONFIG_MAP          # diccionario de clases
from extensions import login_manager                            # LoginManager global
from flask_wtf import CSRFProtect                               # Si usas formularios WTForms

csrf = CSRFProtect()                                            # coméntalo si no usas CSRF


# ───────────────────────────── factory ───────────────────────────
def create_app() -> Flask:
    """Factory Pattern: crea y configura la instancia de Flask."""
    app = Flask(__name__)

    # 1) Configuración según FLASK_ENV ---------------------------
    env = os.getenv("FLASK_ENV", "development").lower()
    app.config.from_object(CONFIG_MAP.get(env, CONFIG_MAP["development"]))

    # 2) Inicializar extensiones ---------------------------------
    login_manager.init_app(app)
    login_manager.login_view = "login.login_page"    # redirección automática 401
    csrf.init_app(app)

    # 3) Registrar blueprints ------------------------------------
    #  ▶ Ruta pública / estática principal
    from routes.main_routes import main_bp           # blueprint = Blueprint("main", ...)
    app.register_blueprint(main_bp)

    #  ▶ Autenticación (usuarios + instituciones)
    from configurations.login_config import login_bp
    app.register_blueprint(login_bp)

    #  ▶ Descomenta los que vayas implementando
    # from routes.docentes_routes       import docente_bp
    # from routes.instituciones_routes  import institucion_bp
    # from routes.student_routes        import student_bp
    #
    # app.register_blueprint(docente_bp)
    # app.register_blueprint(institucion_bp)
    # app.register_blueprint(student_bp)

    # 4) Raíz → portada pública ----------------------------------
    @app.route("/")
    def index():
        # Ajusta al nombre real de tu endpoint público
        # p. ej. main.inicio o main.index
        return redirect(url_for("main.index"))

    # 5) Manejadores de error ------------------------------------
    @app.errorhandler(401)
    def handle_401(_):
        # Cualquier acceso protegido sin sesión → login
        return redirect(url_for("login.login_page"))

    @app.errorhandler(404)
    def handle_404(_):
        return "<h1>404 — Página no encontrada</h1>", 404

    return app


# ─────────────────────────── ejecutar local ──────────────────────
if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(
        debug=flask_app.config["DEBUG"],
        use_reloader=False,        # evita doble proceso en Windows
        host="127.0.0.1",
        port=5000,
    )
