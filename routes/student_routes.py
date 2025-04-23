from flask import Blueprint, render_template

# Crear el Blueprint para la ruta principal
student_bp = Blueprint('student', __name__)

@student_bp.route('/')
def blog ():
    return render_template("student_static/index.html",header_file ="student_footer.html", footer_file ="student_footer.html")

@student_bp.route('/blog')
def class_room ():
    return render_template("student_static/blog.html",header_file ="student_footer.html", footer_file ="student_footer.html")

@student_bp.route('/noticias')
def configurations ():
    return render_template("student_static/noticias.html",header_file ="student_footer.html", footer_file ="student_footer.html")

@student_bp.route('/about-us')
def exams ():
    return render_template("student_static/about_us.html",header_file ="student_footer.html", footer_file ="student_footer.html")

@student_bp.route('/contact-us')
def exersite ():
    return render_template("student_static/contact_us.html",header_file ="student_footer.html", footer_file ="student_footer.html")

@student_bp.route('/contact-us')
def exercite ():
    return render_template("student_static/contact_us.html",header_file ="student_footer.html", footer_file ="student_footer.html")
@student_bp.route('/contact-us')
def foro ():
    return render_template("student_static/contact_us.html",header_file ="student_footer.html", footer_file ="student_footer.html")

@student_bp.route('/contact-us')
def investigation ():
    return render_template("student_static/contact_us.html",header_file ="student_footer.html", footer_file ="student_footer.html")

@student_bp.route('/contact-us')
def personal_profile ():
    return render_template("student_static/contact_us.html",header_file ="student_footer.html", footer_file ="student_footer.html")

@student_bp.route('/contact-us')
def profiles  ():
    return render_template("student_static/contact_us.html",header_file ="student_footer.html", footer_file ="student_footer.html")

