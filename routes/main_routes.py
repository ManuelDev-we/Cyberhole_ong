from flask import Blueprint, render_template

# Crear el Blueprint para la ruta principal
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template("statics/index.html",header_file ="index_header.html", footer_file ="index_footer.html")

@main_bp.route('/blog')
def blog():
    return render_template("statics/blog.html",header_file ="index_header.html", footer_file ="index_footer.html")

@main_bp.route('/noticias')
def noticias():
    return render_template("statics/noticias.html",header_file ="index_header.html", footer_file ="index_footer.html")

@main_bp.route('/about-us')
def about_us():
    return render_template("statics/about_us.html",header_file ="index_header.html", footer_file ="index_footer.html")

@main_bp.route('/contact-us')
def contact_us():
    return render_template("statics/contact_us.html",header_file ="index_header.html", footer_file ="index_footer.html")
# Recursos: Header y Footer para docentes
@main_bp.route('/index-header')
def docente_header():
    return render_template('index_header.html',header_file ="index_header.html", footer_file ="index_footer.html")

@main_bp.route('/index-footer')
def docente_footer():
    return render_template('index_footer.html',header_file ="index_header.html", footer_file ="index_footer.html")

