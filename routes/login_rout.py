from flask import Blueprint, render_template

login_bp = Blueprint('login', __name__)

@login_bp.route('/login_usuario')
def log_in_usuario():
    return render_template(
        'statics/inicio_registro.html',
        header_file="index_header.html",
        footer_file="index_footer.html",
        tipo_registro="usuario"
    )

@login_bp.route('/login_institucion')
def log_in_institucion():
    return render_template(
        'statics/inicio_registro.html',
        header_file="index_header.html",
        footer_file="index_footer.html",
        tipo_registro="institucion"
    )


