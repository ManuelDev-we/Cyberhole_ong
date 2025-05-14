from flask import Flask
from routes.docentes_routes import docentes_routes_bp
from routes.main_routes     import main_bp
from routes.instituciones_routes import institucion_routes_bp
from routes.login_routes     import login_bp          # ⬅ renombrado

app = Flask(__name__)
app.secret_key = "cambia-esto-por-un-secreto-real"    # necesario para sesiones

# Registrar Blueprints (el orden no importa en Flask moderno)
app.register_blueprint(institucion_routes_bp)
app.register_blueprint(login_bp)

app.register_blueprint(docentes_routes_bp)
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)

