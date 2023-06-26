from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Preceptor(db.Model):
    __tablename__= 'preceptor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(120), nullable=False)
    curso = db.relationship('Curso', backref = 'preceptor', cascade= "all, delete-orphan")

class Curso(db.Model):
    __tablename__= 'curso'
    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.Integer, nullable=False)
    division = db.Column(db.Integer, nullable=False)
    idpreceptor = db.Column(db.Integer, db.ForeignKey('preceptor.id'))

class Padre(db.Model):
    __tablename__= 'padre'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(120), nullable=False)   
 

class Estudiante(db.Model):
    __tablename__= 'estudiante'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(10), nullable=False)
    idcurso = db.Column(db.Integer, db.ForeignKey('curso.id'))
    idpadre = db.Column(db.Integer, db.ForeignKey('padre.id'))
    def __gt__(estudiante1,estudiante2):
        return (estudiante1.apellido, estudiante1.nombre)>(estudiante2.apellido, estudiante2.nombre)


class Asistencia(db.Model):
    __tablename__= 'asistencia'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.today())
    codigoclase = db.Column(db.Integer, nullable = False)
    asistio = db.Column(db.String(2), nullable=False)
    justificacion = db.Column(db.String(80))
    idestudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))


