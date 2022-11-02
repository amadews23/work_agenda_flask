from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, TextAreaField, SelectField, BooleanField, PasswordField
from wtforms.fields.html5 import EmailField,  DateTimeField
from wtforms.validators import DataRequired, Required

from aplication.utilidades import EstadoCita

class formPaciente(FlaskForm):
	#id = HiddenField()
	nombre=StringField("Nombre:",validators=[DataRequired("Tienes que introducir el NOMBRE")])
	apellidos=StringField("Apellidos:",validators=[DataRequired("Tienes que introducir los APELLIDOS")])
	dni=StringField("DNI:",default=00,validators=[DataRequired("Tienes que introducir el DNI")])
	email = EmailField('Email')
	telefono1 = StringField("Teléfono1:",default=971,validators=[DataRequired("Tienes que introducir un TELÉFONO")])
	telefono2 = StringField("Teléfono2:",)
	domicilio = StringField("Domicilio:",)
	cp = StringField("Código Postal:",)
	ciudad = StringField("Ciudad:",)
	varios=TextAreaField("Varios:")
	submit = SubmitField('Enviar')


class formCita(FlaskForm):
	fecha_cita=DateTimeField('Fecha de la cita: ', validators=[DataRequired()], format = '%d/%m/%Y')
	hora=DateTimeField('Hora de la cita: ', validators=[DataRequired()])
	precio =DecimalField("Precio:",default=100,validators=[DataRequired("Tienes que introducir el PRECIO")])
	finalizada=SelectField("Finalizada:",coerce=str,choices=EstadoCita.choices())
	facturada=BooleanField("Facturada")
	varios=TextAreaField("Varios:")
	submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Entrar')

class FormUsuario(FlaskForm):
    username = StringField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    nombre = StringField('Nombre completo')
    email = EmailField('Email')
    submit = SubmitField('Aceptar')


class FormChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Aceptar')