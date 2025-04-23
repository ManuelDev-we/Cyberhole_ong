from flask import Blueprint, render_template

# Crear el Blueprint para las rutas de los docentes
docentes_routes_bp = Blueprint('docentes', __name__)

# Gestión con el estudio
@docentes_routes_bp.route('/menu-profesor')
def menu_profesor():
    return render_template('profesor_statics/menu_profesor.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

@docentes_routes_bp.route('/cursos-clases')
def cursos_clases():
    return render_template('profesor_statics/cursos_clases.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

@docentes_routes_bp.route('/proyectos')
def proyectos():
    return render_template('profesor_statics/proyectos.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

@docentes_routes_bp.route('/examen')
def examen():
    return render_template('profesor_statics/examen.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

@docentes_routes_bp.route('/investigacion')
def investigacion():
    return render_template('profesor_statics/investigacion.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

@docentes_routes_bp.route('/class-videos')
def class_videos():
    return render_template('profesor_statics/class_videos.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

@docentes_routes_bp.route('/info-theme')
def info_theme():
    return render_template('profesor_statics/info_theme.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

# Gestión de sponsors
@docentes_routes_bp.route('/sponsors-info')
def sponsors_info():
    return render_template('profesor_statics/sponsors_info.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

@docentes_routes_bp.route('/sponsors-rendimiento')
def sponsors_info_rendimiento():
    return render_template('profesor_statics/sponsors_info_rendimiento.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

# Gestión institucional
@docentes_routes_bp.route('/institucion-info')
def institucion_info():
    return render_template('profesor_statics/institucion_info.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

@docentes_routes_bp.route('/reconocimiento-info')
def reconocimiento_info():
    return render_template('profesor_statics/reconocimiento_info.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

# Recursos: Header y Footer para docentes (opcionalmente, para verlos por separado)
@docentes_routes_bp.route('/docente-header')
def docente_header():
    return render_template('docente_header.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")

@docentes_routes_bp.route('/docente-footer')
def docente_footer():
    return render_template('docente_footer.html', 
                           header_file="docente_header.html", 
                           footer_file="docente_footer.html")
