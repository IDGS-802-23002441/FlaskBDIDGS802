from wtforms import Form, RadioField, StringField, IntegerField
from wtforms import validators
from wtforms.validators import ValidationError, Email

class userform2(Form):
    id = IntegerField('Id')
    nombre = StringField('Nombre', [
        validators.DataRequired(message='Este campo es requerido'),
        validators.Length(min=4, max=50)])
    apellidos = StringField('Apellido', [validators.Length(min=4, max=50)])
    email = StringField('Email', [
        validators.DataRequired(message='El email es requerido'),
        validators.Email(message='Ingrese un correo válido')])
    telefono = StringField('Telefono', [validators.Length(min=10, max = 20)])
