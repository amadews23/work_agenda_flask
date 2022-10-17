import datetime

from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from aplication import config
from aplication.forms import formPaciente, formCita
from aplication.utilidades import lista_letras_mayusculas, EstadoCita
from werkzeug.utils import redirect

app = Flask(__name__,template_folder='../templates')
app.config.from_object(config)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
Bootstrap(app)
db = SQLAlchemy(app)

#TODO Poder CAMBIAR el CLIENTE en una cita nueva y en modificar cita
#TODO Poder ir a CREAR cita desde la lista de citas
#TODO Revisar botones aun no "implementados del todo" en:
# http://127.0.0.1:5000/cita/nueva/paciente/<idcita>
# http://127.0.0.1:5000/paciente/modificar/<idpaciente>
# http://127.0.0.1:5000/ crear cita


'''Esta lista nos indica como mostrar la lista de botones 1->Desde citas y 2->Desde paciente'''
tipo_botones_lista_citas=[1,2]

from aplication.models import Pacientes, Citas, Facturas

@app.route('/')
@app.route('/citas_paciente/<id>')
@app.route('/citas_finalizadas/<fin>')
@app.route('/citas_facturadas/<fact>')
def inicio(id='0', fin='0', fact='0' ):

	tipo_botones=tipo_botones_lista_citas[0]

	paciente=Pacientes.query.get(id)
	#TODO Arreglar logica para busquedas finalizadas - canceladas -pendientes Y Facturadas

	if id=='0' and fin=='0' and fact =='0':
		citas=Citas.query.all()

	elif fin=='1':
		citas=Citas.query.filter_by(finalizada=EstadoCita.PENDIENTE)

	elif fin=='2':
		citas=Citas.query.filter_by(finalizada=EstadoCita.CANCELADA)

	elif fin=='3':
		citas=Citas.query.filter_by(finalizada=EstadoCita.FINALIZADA)

	elif fact=='1':
		citas=Citas.query.filter_by(facturada=False)

	elif fact=='2':
		citas=Citas.query.filter_by(facturada=True)

	else:
		citas=Citas.query.filter_by(paciente_id=id)

	pacientes=Pacientes.query.all()
	return render_template("inicio.html",citas=citas,pacientes=pacientes,paciente=paciente,EstadoCita=EstadoCita, tipo_botones=tipo_botones)

@app.route('/paciente/<id>')
@app.route('/paciente/<id>/citas_finalizadas/<fin>')
@app.route('/paciente/<id>/citas_facturadas/<fact>')
def paciente(id,fin=0,fact=0):
	tipo_botones=tipo_botones_lista_citas[1]

	paciente=Pacientes.query.get(id)

	if fin=='1':
		citas = Citas.query.filter_by(paciente_id=id,finalizada=EstadoCita.PENDIENTE)

	elif fin=='2':
		citas = Citas.query.filter_by(paciente_id=id,finalizada=EstadoCita.CANCELADA)

	elif fin=='3':
		citas = Citas.query.filter_by(paciente_id=id, finalizada=EstadoCita.FINALIZADA)

	elif fact=='1':
		citas = Citas.query.filter_by(paciente_id=id, facturada=False)

	elif fact=='2':
		citas = Citas.query.filter_by(paciente_id=id, facturada=True)

	else:
		citas = Citas.query.filter_by(paciente_id=id)

	return render_template("paciente.html",paciente=paciente, citas=citas, EstadoCita=EstadoCita, mostrar_lista_paciente='0', tipo_botones=tipo_botones)

@app.route('/pacientes')
@app.route('/pacientes/letra/apellido/<lap>')
@app.route('/pacientes/letra/nombre/<lnom>')
def pacientes(lap='0', lnom='0'):

	if lap=='0' and lnom=='0':
		pacientes=Pacientes.query.all()
	else:
		if lap!='0':
			pacientes = db.session.query(Pacientes).filter(Pacientes.apellidos.like(lap+'%'))
		if lnom!='0':
			pacientes = db.session.query(Pacientes).filter(Pacientes.nombre.like(lnom+'%'))

	listamayusculas=lista_letras_mayusculas()

	return render_template("pacientes.html",pacientes=pacientes, listamayusculas=listamayusculas)


@app.route('/paciente/modificar/<id>', methods=["get","post"])
@app.route('/paciente/nuevo', methods=["get","post"])
def paciente_edit(id=0):

	form = formPaciente()

	#SUBMIT para un NUEVO paciente
	if form.validate_on_submit() and id==0 and request.form['id_paciente'] =='0':

		paciente = Pacientes()
		form.populate_obj(paciente)
		db.session.add(paciente)
		db.session.commit()

		return redirect(url_for("pacientes"))

	#SUBMIT para EDITAR paciente
	elif form.validate_on_submit() :

		paciente = Pacientes.query.get(request.form['id_paciente'])
		form.populate_obj(paciente)
		db.session.commit()

		return redirect(url_for("paciente", id=request.form['id_paciente']))

	#GENERAR formulario para EDITAR paciente
	elif id != 0:

		paciente = Pacientes.query.get(id)
		form=formPaciente(obj=paciente)
		return render_template("paciente_edit.html", form=form, id=id)

	#GENERAR formulario para NUEVO paciente
	else:
		return render_template("paciente_edit.html",form=form, id=id)

@app.route('/cita/modificar/<id>', methods=["get","post"])
@app.route('/cita/nueva/paciente/<idpac>', methods=["get","post"])
@app.route('/cita/nueva', methods=["get","post"])
def cita_edit(id=0, idpac=0):

	form = formCita()

	#SUBMIT para MODIFICAR cita
	if request.method=="POST" and request.form['id_cita'] != '0':

		cita = Citas.query.get(request.form['id_cita'])

		form.populate_obj(cita)

		cita.fecha_cita = datetime.datetime(int(request.form['fecha_cita'][0:4]),int(request.form['fecha_cita'][5:7]),
											int(request.form['fecha_cita'][8:]), int(request.form['hora'][0:2]),
											int(request.form['hora'][3:]))

		cita.finalizada =  EstadoCita.from_name(request.form['finalizada'])

		db.session.commit()

		return redirect(url_for("inicio"))

	#SUBMIT para un NUEVA cita Paciente
	if request.method=="POST" and request.form['id_cita'] == '0':
		print("POST")
		cita = Citas()
		cita.paciente_id= request.form['id_paciente']

		#print(request.form['fecha_cita'][0:4]) #anyo
		#print(request.form['fecha_cita'][5:7]) #mes
		#print(request.form['fecha_cita'][8:]) #dia
		#print(request.form['hora'][0:2]) #hora
		#print(request.form['hora'][3:]) #minuto

		form.populate_obj(cita)
		cita.fecha_cita = datetime.datetime(int(request.form['fecha_cita'][0:4]),int(request.form['fecha_cita'][5:7]),
											int(request.form['fecha_cita'][8:]), int(request.form['hora'][0:2]),
											int(request.form['hora'][3:]))

		cita.fecha_creacion = datetime.datetime.now()

		cita.finalizada =  EstadoCita.from_name(request.form['finalizada'])

		db.session.add(cita)
		db.session.commit()

		return redirect(url_for("inicio"))

	#GENERAR formulario para CREAR cita de paciente
	elif id == 0 and idpac != 0:

		#print("GET para CREAR cita para PACIENTE")
		paciente = Pacientes.query.get(idpac)

		return render_template("cita_edit.html", form=form, paciente=paciente, id_cita='0', idpac=idpac)


	#GENERAR formulario para MODIFICAR cita
	else:

		#print("GET para MODIFICAR cita para PACIENTE")
		cita = Citas.query.get(id)
		form=formCita(obj=cita)

		paciente=Pacientes.query.get(cita.paciente_id)

		return render_template("cita_edit.html",form=form,paciente=paciente, id_cita=cita.id,idpac=cita.paciente_id,
							   fecha_cita=cita.fecha_cita.strftime("%Y-%m-%d")
							   ,hora_cita=cita.fecha_cita.strftime("%H:%M"))

@app.errorhandler(404)
def page_not_found(error):
	return render_template("error.html",error="Página no encontrada..."), 404
