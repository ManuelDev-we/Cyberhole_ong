# student_routes.py
from flask import Blueprint, render_template

student_bp = Blueprint(
    'student',
    __name__,
    url_prefix='/student',
    template_folder='student_static'
)

@student_bp.route('/')
def index_student():
    return render_template('index.html')

@student_bp.route('/blog')
def student_blog():
    return render_template('blog.html')

@student_bp.route('/noticias')
def student_noticias():
    return render_template('noticias.html')

@student_bp.route('/about-us')
def student_about_us():
    return render_template('about_us.html')

@student_bp.route('/contact-us')
def student_contact_us():
    return render_template('contact_us.html')
