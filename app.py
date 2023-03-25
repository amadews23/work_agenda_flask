import datetime

from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from aplication import config
from aplication.forms import formPaciente, formCita, LoginForm, FormUsuario, FormChangePassword
from aplication.utilidades import EstadoCita, devolver_lista_mayusculas, devolver_numero_paginas

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
Bootstrap(app)
db = SQLAlchemy(app)

# TODO Poder CAMBIAR el CLIENTE en una cita nueva y en modificar cita
# TODO Poder ir a CREAR cita desde la lista de citas
# TODO Revisar botones aun no "implementados del todo" en:
# http://127.0.0.1:5000/cita/nueva/paciente/<idcita>
# http://127.0.0.1:5000/paciente/modificar/<idpaciente>
# http://127.0.0.1:5000/ crear cita


'''Esta lista nos indica como mostrar la lista de botones 1->Desde citas y 2->Desde paciente'''
tipo_botones_lista_citas = [1, 2]

from aplication.models import Pacientes, Citas

@app.route('/')
def home():
    return redirect(url_for("inicio"))


@app.route('/citas_todas/')
@app.route('/citas_todas/<npag>/')
@app.route('/citas_paciente/<id>/')
@app.route('/citas_paciente/<id>/<npag>/')
@app.route('/citas_finalizadas/<fin>/')
@app.route('/citas_finalizadas/<fin>/<npag>/')
@app.route('/citas_facturadas/<fact>/')
@app.route('/citas_facturadas/<fact>/<npag>/')

def inicio(id='0',
           fin='0',
           fact='0',
           npag='0'):

    tipo_botones = tipo_botones_lista_citas[0]

    paciente = Pacientes.query.get(id)

    # TODO Arreglar logica para busquedas finalizadas - canceladas -pendientes Y Facturadas

    c = Citas.query
    ruta_inicial = "citas_todas/"

    if id == '0' and fin == '0' and fact == '0':

        citas = c.filter_by()#c.all()
        #print(c.count())
        n_total_citas = c.count()

    elif fin == '1':
        citas = c.filter_by(finalizada=EstadoCita.PENDIENTE)
        #print(citas.count())
        n_total_citas = citas.count()
        ruta_inicial = "citas_finalizadas/"+fin+"/"

    elif fin == '2':
        citas = c.filter_by(finalizada=EstadoCita.CANCELADA)
        #print(citas.count())
        n_total_citas = citas.count()
        ruta_inicial = "citas_finalizadas/"+fin+"/"


    elif fin == '3':
        citas = c.filter_by(finalizada=EstadoCita.FINALIZADA)
        #print(citas.count())
        n_total_citas = citas.count()
        ruta_inicial = "citas_finalizadas/"+fin+"/"


    elif fact == '1':
        citas = c.filter_by(facturada=False)
        #print(citas.count())
        n_total_citas = citas.count()
        ruta_inicial = "citas_facturadas/"+fact+"/"


    elif fact == '2':
        citas = c.filter_by(facturada=True)
        #print(citas.count())
        n_total_citas = citas.count()
        ruta_inicial = "citas_facturadas/"+fact+"/"

    else:
        citas = c.filter_by(paciente_id=id)
        #print(citas.count())
        n_total_citas = citas.count()
        ruta_inicial = "citas_paciente/"+"id"+"/"

    #print(devolver_numero_paginas(n_total_citas, 5))
    #pacientes = Pacientes.query.all()
    #print( url_for(request.endpoint))
    return render_template("inicio.html",
                           citas=citas.paginate(int(npag), 5, False).items,
                           #pacientes=pacientes,
                           paciente=paciente,
                           EstadoCita=EstadoCita,
                           tipo_botones=tipo_botones,
                           n_paginas=devolver_numero_paginas(n_total_citas, 5),
                           ruta_inicial=ruta_inicial,
                           npag = int(npag)
                           )


@app.route('/paciente/<id>')
@app.route('/paciente/<id>/citas_finalizadas/<fin>')
@app.route('/paciente/<id>/citas_facturadas/<fact>')
def paciente(id, fin=0, fact=0):

    c = Citas.query


    tipo_botones = tipo_botones_lista_citas[1]

    paciente = Pacientes.query.get(id)

    if fin == '1':
        citas = c.filter_by(paciente_id=id, finalizada=EstadoCita.PENDIENTE)
        n_total_citas = citas.count()


    elif fin == '2':
        citas = c.filter_by(paciente_id=id, finalizada=EstadoCita.CANCELADA)
        n_total_citas = citas.count()

    elif fin == '3':
        citas = c.filter_by(paciente_id=id, finalizada=EstadoCita.FINALIZADA)
        n_total_citas = citas.count()

    elif fact == '1':
        citas = c.filter_by(paciente_id=id, facturada=False)
        n_total_citas = citas.count()

    elif fact == '2':
        citas = c.filter_by(paciente_id=id, facturada=True)
        n_total_citas = citas.count()

    else:
        citas = c.filter_by(paciente_id=id)
        n_total_citas = citas.count()

    return render_template("paciente.html",
                           paciente=paciente,
                           citas=citas,
                           EstadoCita=EstadoCita,
                           mostrar_lista_paciente='0',
                           tipo_botones=tipo_botones,
                           n_paginas=devolver_numero_paginas(n_total_citas, 5)
                           )


@app.route('/pacientes/')
@app.route('/pacientes/<npag>/')
@app.route('/pacientes/letra/apellido/<lap>/')
@app.route('/pacientes/letra/apellido/<lap>/<npag>/')
@app.route('/pacientes/letra/nombre/<lnom>/')
@app.route('/pacientes/letra/nombre/<lnom>/<npag>/')
def pacientes(lap='0',
              lnom='0',
              npag='0'):

    p = Pacientes.query
    if lap == '0' and lnom == '0':
        pacientes = p.filter()
        ruta_inicial = "pacientes/"
        n_total_pacientes = pacientes.count()

    else:
        if lap != '0':
            pacientes = p.filter(Pacientes.apellidos.like(lap + '%'))
            ruta_inicial = "pacientes/letra/apellido/"+lap+"/"
            n_total_pacientes = pacientes.count()

        if lnom != '0':
            pacientes = p.filter(Pacientes.nombre.like(lnom + '%'))
            ruta_inicial = "pacientes/nombre/apellido/"+lap+"/"
            n_total_pacientes = pacientes.count()

    return render_template("pacientes.html",
                           pacientes=pacientes.paginate(int(npag), 5, False).items,
                           listamayusculas=devolver_lista_mayusculas(),
                           n_paginas=devolver_numero_paginas(n_total_pacientes, 5),
                           ruta_inicial=ruta_inicial,
                           npag=int(npag)
                           )


@app.route('/paciente/modificar/<id>', methods=["get", "post"])
@app.route('/paciente/nuevo', methods=["get", "post"])
def paciente_edit(id=0):
    form = formPaciente()

    # SUBMIT para un NUEVO paciente
    if form.validate_on_submit() and id == 0 and request.form['id_paciente'] == '0':

        paciente = Pacientes()
        form.populate_obj(paciente)
        db.session.add(paciente)
        db.session.commit()

        return redirect(url_for("pacientes"))

    # SUBMIT para EDITAR paciente
    elif form.validate_on_submit():

        paciente = Pacientes.query.get(request.form['id_paciente'])
        form.populate_obj(paciente)
        db.session.commit()

        return redirect(url_for("paciente", id=request.form['id_paciente']))

    # GENERAR formulario para EDITAR paciente
    elif id != 0:

        paciente = Pacientes.query.get(id)
        form = formPaciente(obj=paciente)
        return render_template("paciente_edit.html", form=form, id=id)

    # GENERAR formulario para NUEVO paciente
    else:
        return render_template("paciente_edit.html", form=form, id=id)


@app.route('/cita/modificar/<id>', methods=["get", "post"])
@app.route('/cita/nueva/paciente/<idpac>', methods=["get", "post"])
@app.route('/cita/nueva', methods=["get", "post"])
def cita_edit(id=0, idpac=0):
    form = formCita()
    # SUBMIT para MODIFICAR cita
    if request.method == "POST" and request.form['id_cita'] != '0':
        cita = Citas.query.get(request.form['id_cita'])

        form.populate_obj(cita)

        cita.fecha_cita = datetime.datetime(int(request.form['fecha_cita'][0:4]), int(request.form['fecha_cita'][5:7]),
                                            int(request.form['fecha_cita'][8:]), int(request.form['hora'][0:2]),
                                            int(request.form['hora'][3:]))

        cita.finalizada = EstadoCita.from_name(request.form['finalizada'])

        db.session.commit()

        return redirect(url_for("inicio"))

    # SUBMIT para un NUEVA cita Paciente
    if request.method == "POST" and request.form['id_cita'] == '0':
        print("POST")
        cita = Citas()
        cita.paciente_id = request.form['id_paciente']

        # print(request.form['fecha_cita'][0:4]) #anyo
        # print(request.form['fecha_cita'][5:7]) #mes
        # print(request.form['fecha_cita'][8:]) #dia
        # print(request.form['hora'][0:2]) #hora
        # print(request.form['hora'][3:]) #minuto

        form.populate_obj(cita)
        cita.fecha_cita = datetime.datetime(int(request.form['fecha_cita'][0:4]),
                                            int(request.form['fecha_cita'][5:7]),
                                            int(request.form['fecha_cita'][8:]),
                                            int(request.form['hora'][0:2]),
                                            int(request.form['hora'][3:]))

        cita.fecha_creacion = datetime.datetime.now()

        cita.finalizada = EstadoCita.from_name(request.form['finalizada'])

        db.session.add(cita)
        db.session.commit()

        return redirect(url_for("inicio"))

    # GENERAR formulario para CREAR cita de paciente
    elif id == 0 and idpac != 0:

        # print("GET para CREAR cita para PACIENTE")
        paciente = Pacientes.query.get(idpac)

        return render_template("cita_edit.html", form=form, paciente=paciente, id_cita='0', idpac=idpac)

    # GENERAR formulario para MODIFICAR cita TODO

    else:
        # print("GET para MODIFICAR cita para PACIENTE")
        cita = Citas.query.get(id)

        form = formCita(obj=cita)
        print(cita.paciente_id)

        paciente = Pacientes.query.get(cita.paciente_id)
        return render_template("cita_edit.html",
                               form=form,
                               paciente=paciente,
                               id_cita=cita.id,
                               idpac=cita.paciente_id,
                               fecha_cita=cita.fecha_cita.strftime("%Y-%m-%d"),
                               hora_cita=cita.fecha_cita.strftime("%H:%M"),
                               listamayusculas=devolver_lista_mayusculas(),
                               pacientes=Pacientes.query.paginate(2, 10, False).items)
        # all())


@app.route('/login', methods=['get', 'post'])
def login():
    from aplication.models import Usuarios
    from aplication.login import login_user
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('inicio'))
        form.username.errors.append("Usuario o contraseña incorrectas.")
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    from aplication.login import logout_user
    logout_user()
    return redirect(url_for('login'))


@app.route("/registro", methods=["get", "post"])
def registro():
    from aplication.models import Usuarios
    form = FormUsuario()
    if form.validate_on_submit():
        existe_usuario = Usuarios.query. \
            filter_by(username=form.username.data).first()
        if existe_usuario is None:
            user = Usuarios()
            form.populate_obj(user)
            user.admin = False
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("inicio"))
        form.username.errors.append("Nombre de usuario ya existe.")
    return render_template("usuarios_new.html", form=form)


@app.route('/perfil/<username>', methods=["get", "post"])
def perfil(username):
    from aplication.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = FormUsuario(request.form, obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("usuarios_new.html", form=form, perfil=True)


@app.route('/changepassword/<username>', methods=["get", "post"])
def changepassword(username):
    from aplication.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = FormChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("changepassword.html", form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404
