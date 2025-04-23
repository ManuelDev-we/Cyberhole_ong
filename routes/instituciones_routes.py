
from flask import Blueprint, render_template

# Crear el Blueprint para las rutas de los institucions
institucion_routes_bp = Blueprint('institucions', __name__)

# Gestión con el estudio
@institucion_routes_bp.route('/menu-profesor')
def blog_institucion ():
    return render_template('institution_statics/menu_profesor.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

@institucion_routes_bp.route('/cursos-clases')
def configuracion_institucion():
    return render_template('institution_statics/cursos_clases.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

@institucion_routes_bp.route('/proyectos')
def proyectos():
    return render_template('institution_statics/proyectos.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

@institucion_routes_bp.route('/examen')
def examen():
    return render_template('institution_statics/examen.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

@institucion_routes_bp.route('/investigacion')
def investigacion():
    return render_template('institution_statics/investigacion.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

@institucion_routes_bp.route('/class-videos')
def class_videos():
    return render_template('institution_statics/class_videos.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

@institucion_routes_bp.route('/info-theme')
def info_theme():
    return render_template('institution_statics/info_theme.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

# Gestión de sponsors
@institucion_routes_bp.route('/sponsors-info')
def sponsors_info():
    return render_template('institution_statics/sponsors_info.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

@institucion_routes_bp.route('/sponsors-rendimiento')
def sponsors_info_rendimiento():
    return render_template('institution_statics/sponsors_info_rendimiento.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

# Gestión institucional
@institucion_routes_bp.route('/institucion-info')
def institucion_info():
    return render_template('institution_statics/institucion_info.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

@institucion_routes_bp.route('/reconocimiento-info')
def reconocimiento_info():
    return render_template('institution_statics/reconocimiento_info.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

# Recursos: Header y Footer para institucions (opcionalmente, para verlos por separado)
@institucion_routes_bp.route('/institucion-header')
def institucion_header():
    return render_template('institucion_header.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

@institucion_routes_bp.route('/institucion-footer')
def institucion_footer():
    return render_template('institucion_footer.html', 
                           header_file="institucion_header.html", 
                           footer_file="institucion_footer.html")

