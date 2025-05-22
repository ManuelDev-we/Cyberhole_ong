# institucion_routes.py
from flask import Blueprint, render_template

institucion_bp = Blueprint(
    'institucion',
    __name__,
    url_prefix='/institucion',
    template_folder='institucion_static'
)

@institucion_bp.route('/')
def index_institucion():
    return render_template('index.html')

@institucion_bp.route('/perfil')
def institucion_perfil():
    return render_template('perfil.html')

@institucion_bp.route('/autorizaciones')
def institucion_autorizaciones():
    return render_template('autorizaciones.html')

@institucion_bp.route('/carreras')
def institucion_carreras():
    return render_template('carreras.html')
