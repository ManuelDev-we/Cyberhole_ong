import getpass
import bcrypt

# Base de datos simulada (en memoria)
usuarios_registrados = {}

# Clases
class Usuario:
    def __init__(self, nombre, correo, password_hash):
        self.nombre = nombre
        self.correo = correo
        self.password_hash = password_hash

    def evolucionar_a_docente(self):
        return Docente(self.nombre, self.correo, self.password_hash)

    def evolucionar_a_estudiante(self):
        return Estudiante(self.nombre, self.correo, self.password_hash)

class Docente(Usuario):
    def __init__(self, nombre, correo, password_hash):
        super().__init__(nombre, correo, password_hash)
        self.cursos = []

    def crear_curso(self, titulo, descripcion):
        nuevo_curso = Curso(titulo, descripcion, self)
        self.cursos.append(nuevo_curso)
        return nuevo_curso

class Estudiante(Usuario):
    def __init__(self, nombre, correo, password_hash):
        super().__init__(nombre, correo, password_hash)
        self.certificaciones = []

    def obtener_certificacion(self, curso):
        certificacion = Certificacion(self, curso)
        self.certificaciones.append(certificacion)
        return certificacion

class Curso:
    def __init__(self, titulo, descripcion, docente):
        self.titulo = titulo
        self.descripcion = descripcion
        self.docente = docente

class Certificacion:
    def __init__(self, estudiante, curso):
        self.estudiante = estudiante
        self.curso = curso

    def mostrar(self):
        return f"{self.estudiante.nombre} está certificado en '{self.curso.titulo}' por el docente {self.curso.docente.nombre}"

# Función para registrar
def registrar_usuario():
    nombre = input("Nombre: ")
    correo = input("Correo: ")

    if correo in usuarios_registrados:
        print("Este correo ya está registrado.")
        return None

    password = getpass.getpass("Contraseña: ")
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    nuevo_usuario = Usuario(nombre, correo, password_hash)
    usuarios_registrados[correo] = nuevo_usuario
    print("Registro exitoso.")

# Función para ingresar
def ingresar_usuario():
    correo = input("Correo: ")
    password = getpass.getpass("Contraseña: ")

    usuario = usuarios_registrados.get(correo)
    if not usuario:
        print("Usuario no encontrado.")
        return None

    if bcrypt.checkpw(password.encode(), usuario.password_hash):
        print(f"Bienvenido {usuario.nombre}")
        return usuario
    else:
        print("Contraseña incorrecta.")
        return None