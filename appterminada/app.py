from datetime import datetime
from flask import Flask, request, render_template, session as flask_session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


app = Flask(__name__)
app.config.from_pyfile('config.py')

from clases import db
from clases import Asistencia, Preceptor, Padre, Curso, Estudiante

@app.route('/', methods = ['GET','POST'])
def iniciar_sesion():
    if request.method == 'POST':
        if not request.form['correo'] or not request.form['clave'] or not request.form['rol']:
            return render_template('error.html',error="Los datos ingresados no son correctos.")
        else:
            rol=request.form['rol']
            if rol == 'Padre':
                actual = Padre.query.filter_by( correo= request.form['correo']).first()
                if actual is None:
                    return render_template('error.html', error='El correo ingresado no existe')
                else:
                    c = request.form['clave']
                    result = hashlib.md5(c.encode()).hexdigest()
                    flask_session['userid'] = actual.id
                    if (actual.clave == result):
                        return render_template('index2.html')
                    else:
                        return render_template('error.html', error="La contraseña no es valida")
            elif rol == 'Preceptor':
                actual = Preceptor.query.filter_by(correo=request.form['correo']).first()
                if actual is None:
                    return render_template('error.html', error='El correo ingresado no existe')
                else:
                    c = request.form['clave']
                    result = hashlib.md5(c.encode()).hexdigest()
                    flask_session['userid'] = actual.id
                    if (actual.clave == result):
                        return render_template('index.html')
                    else:
                        return render_template('error.html', error="La contraseña no es valida")
            else:
                return render_template('error.html', error = "El rol seleccionado es erroneo")
    else:
        return render_template('iniciar_sesion.html')
@app.route('/index' , methods = ['GET','POST'])
def index():
    return render_template('index.html')
@app.route('/index2', methods = ['GET','POST'])
def index2():
    return render_template('index2.html')
@app.route('/registrar_asistencia', methods=['GET', 'POST'])
def registrar_asistencia():
    if 'userid' in flask_session:
        user_id = flask_session['userid']
        actual = Preceptor.query.get(user_id)
        if request.method == 'POST':
            if 'curso' not in request.form:
                return render_template('registrar_asistencia.html', cursos=Curso.query.all(), curso_selecc=None, preceptor=actual)
            else:
                curso_id = request.form['curso']
                curso_selecc = Curso.query.get(curso_id)
                estudiantes = Estudiante.query.filter_by(idcurso=curso_selecc.id).all()
                estudiantes.sort()
                render_template('registrar_asistencia.html', cursos=None, curso_selecc=curso_selecc, preceptor=actual, estudiantes=estudiantes)
                for estudiante in estudiantes:
                    clase = request.form.get('clase')
                    print(clase)
                    asistenciaa = request.form.get('asistio')
                    print(asistenciaa)
                    justificacion = request.form.get('justificacion')
                    print(justificacion)
                    nueva_asistencia = Asistencia(fecha=datetime.today(),codigoclase=clase,asistio=asistenciaa,justificacion=justificacion,idestudiante=estudiante.id)
                    db.session.add(nueva_asistencia)
                db.session.commit()
                return render_template('registrar_asistencia.html', cursos=None, curso_selecc=curso_selecc, preceptor=actual, estudiantes=estudiantes)
        else:
            return render_template('registrar_asistencia.html', cursos=Curso.query.all(), curso_selecc=None, preceptor=actual)
    else:
        return render_template('error.html', error='Debe iniciar sesión como preceptor para acceder a esta página.')


@app.route('/obtener_informe', methods=['GET', 'POST'])
def obtener_informe():
    informe = []
    if 'userid' in flask_session:
        user_id = flask_session['userid']
        actual = Preceptor.query.get(user_id)
        if request.method == 'POST':
            if not request.form['curso']:
                return render_template('obtener_informe.html', cursos=Curso.query.all(), curso_selecc=None, preceptor=actual)
            else:
                curso_id = request.form['curso']
                curso_selecc = Curso.query.get(curso_id)
                estudiantes = Estudiante.query.filter_by(idcurso=curso_selecc.id).all()
                estudiantes.sort()
                for estudiante in estudiantes:
                    ctotal=0
                    asistencias = Asistencia.query.filter_by(idestudiante=estudiante.id).all()
                    clases_aula_presentes = sum(1 for asistencia in asistencias if asistencia.asistio=='s' and asistencia.codigoclase == 1)
                    clases_edu_fis_presentes = sum(1 for asistencia in asistencias if asistencia.asistio=='s' and asistencia.codigoclase == 2)
                    clases_aula_aus_justificadas = sum(1 for asistencia in asistencias if  asistencia.asistio=='n' and asistencia.justificacion!=None and asistencia.codigoclase == 1)    
                    clases_aula_aus_injustificadas = sum(1 for asistencia in asistencias if  asistencia.asistio=='n' and asistencia.justificacion==None and asistencia.codigoclase == 1) 
                    clases_edu_aus_justificadas = sum(1 for asistencia in asistencias if  asistencia.asistio=='n' and asistencia.justificacion!=None and asistencia.codigoclase == 2)    
                    clases_edu_aus_injustificadas = sum(1 for asistencia in asistencias if  asistencia.asistio=='n' and asistencia.justificacion==None and asistencia.codigoclase == 2)  
                    for asistencia in asistencias:
                        if  asistencia.asistio=='n' and asistencia.justificacion!=None and asistencia.codigoclase == 1:
                            ctotal+=1
                        if  asistencia.asistio=='n' and asistencia.justificacion==None and asistencia.codigoclase == 1:
                            ctotal+=1
                        if  asistencia.asistio=='n' and asistencia.justificacion!=None and asistencia.codigoclase == 2:
                            ctotal+=0.5
                        if  asistencia.asistio=='n' and asistencia.justificacion==None and asistencia.codigoclase == 2:
                            ctotal+=0.5
                        
                    estudiante_info = {
                    'apellido': estudiante.apellido,
                    'nombre': estudiante.nombre,
                    'clases_aula_presentes': clases_aula_presentes,
                    'clases_edu_fis_presentes': clases_edu_fis_presentes,
                    'clases_aula_aus_justificadas': clases_aula_aus_justificadas,
                    'clases_aula_aus_injustificadas':clases_aula_aus_injustificadas,
                    'clases_edu_aus_justificadas':clases_edu_aus_justificadas,
                    'clases_edu_aus_injustificadas':clases_edu_aus_injustificadas,
                    'total_de_inasistencias':ctotal
                    }

                    informe.append(estudiante_info)

                return render_template('obtener_informe.html', cursos=None, curso_selecc=curso_selecc, preceptor=actual,informe=informe)
        else:
            return render_template('obtener_informe.html', cursos=Curso.query.all(), curso_selecc=None, preceptor=actual)
    else:
        return render_template('error.html', error='Debe iniciar sesión como preceptor para acceder a esta página.')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)