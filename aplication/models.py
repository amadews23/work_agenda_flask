from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Float
from sqlalchemy.orm import relationship
from aplication.app import db
from aplication.utilidades import EstadoCita


#def order_by(model, field):
#	''''stmt = select([users_table]).order_by(desc(users_table.c.name))
#	stmt = select([model]).order_by(desc(field))
#	print(model.__tablename__)
#	print(field)
#	print (stmt)


class Pacientes(db.Model):

	__tablename__ = 'pacientes'
	id = Column(Integer, primary_key=True)
	nombre = Column(String(100),nullable=False)
	apellidos = Column(String(200),nullable=False)
	dni = Column(String(10),nullable=False)
	telefono1 = Column(String(9),nullable=False)
	telefono2 = Column(String(9),nullable=False)
	email = Column(String(100))
	domicilio = Column(String(200))
	cp = Column(String(6))
	ciudad = Column(String(200))
	varios = Column(String(300))

	def numero_visitas(self,id):
		return Citas.query.filter_by(paciente_id=self.id).count()

	def primera_visita(self,id):

		#return Citas.query.filter_by(paciente_id=self.id).with_entities(Citas.fecha_cita).first()
		return Citas.query.filter_by(paciente_id=self.id).with_entities(Citas.fecha_cita).order_by(Citas.fecha_cita).first()

	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class Citas(db.Model):

	__tablename__ = 'citas'
	id = Column(Integer, primary_key=True)
	fecha_creacion = Column(DateTime, default=datetime.utcnow)
	fecha_cita = Column(DateTime)
	precio = Column(Float,default=0)
	finalizada = Column(db.Enum(EstadoCita))
	facturada = Column(Boolean, default=False)
	varios = Column(String(300))
	paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
	pacientes = relationship("Pacientes", backref="Citas",lazy=True)

	def __repr__(self):
	    return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))


class Facturas(db.Model):

	id = Column(Integer, primary_key=True)
	numero_factura = Column(Integer,default=0)
	#fecha = Column(DateTime)
	#CitaId = Column(Integer, ForeignKey('citas.id'), nullable=False)
	#cita = relationship("Facturas", backref="Citas",lazy='dynamic')

	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
