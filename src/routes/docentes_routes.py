# docente_routes.py
from flask import Blueprint, render_template

docente_bp = Blueprint(
    'docente',
    __name__,
    url_prefix='/docente',
    template_folder='docente_static'
)

@docente_bp.route('/')
def index_docente():
    return render_template('index.html')

@docente_bp.route('/perfil')
def docente_perfil():
    return render_template('perfil.html')

@docente_bp.route('/clases')
def docente_clases():
    return render_template('clases.html')

@docente_bp.route('/examenes')
def docente_examenes():
    return render_template('examenes.html')
