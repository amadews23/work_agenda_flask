import datetime

from flask_script import Manager
from aplication.app import app,db
from aplication.models import Citas, Pacientes, EstadoCita

manager = Manager(app)
app.config['DEBUG'] = True # Ensure debugger will load.

@manager.command
def create_tables():
    "Create relational database tables."
    db.create_all()
    paciente=Pacientes(nombre="BME", apellidos="V", dni="40123123E", telefono1="971000000", telefono2="871000000")
    db.session.add(paciente)
    paciente2=Pacientes(nombre="Javier", apellidos="Cuenc", dni="44123123X", telefono1="971111111", telefono2="871111111")
    db.session.add(paciente2)
    paciente3=Pacientes(nombre="Pepe", apellidos="Gotera", dni="45123123R", telefono1="971222222", telefono2="871222222")
    db.session.add(paciente3)
    paciente4=Pacientes(nombre="Juan Carlos", apellidos="Gómez", dni="46123123T", telefono1="9713333333", telefono2="8713333333")
    db.session.add(paciente4)
    cita=Citas(fecha_creacion= datetime.datetime(2019, 4, 19, 0, 0), fecha_cita= datetime.datetime(2019, 4, 19, 0, 0), precio=100, finalizada=EstadoCita.PENDIENTE, facturada=False, paciente_id=1)
    db.session.add(cita)
    cita2=Citas(fecha_creacion= datetime.datetime(2020, 2, 19, 0, 0), fecha_cita= datetime.datetime(2020, 2, 19, 0, 0), precio=100, finalizada=EstadoCita.CANCELADA, facturada=False, paciente_id=2)
    db.session.add(cita2)
    cita3=Citas(fecha_creacion= datetime.datetime.now(), fecha_cita= datetime.datetime.now(), precio=100, finalizada=EstadoCita.FINALIZADA, facturada=False, paciente_id=3)
    db.session.add(cita3)

    db.session.commit()

@manager.command
def add_data_tables():
    db.create_all()


if __name__ == '__main__':
	manager.run()
