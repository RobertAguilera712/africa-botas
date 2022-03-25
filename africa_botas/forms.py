from email import message
from flask_wtf import FlaskForm
from africa_botas import mongo
from wtforms import * 
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, NumberRange

class LoginForm(FlaskForm):
    usuario = StringField(label='Usuario', validators=[DataRequired('Por favor introduzca el usuario')])
    password = PasswordField(label='Contraseña', validators=[DataRequired('Por favor introduzca la contraseña')])
    submit = SubmitField(label='Iniciar Sesión')

class RegistrarEmpleadoForm(FlaskForm):
    nombre = StringField(label='Nombre', validators=[DataRequired('Por favor introduzca el nombre')])
    apellido_p = StringField(label='Apellido paterno', validators=[DataRequired('Por favor introduzca el primer apellido')])
    apellido_m = StringField(label='Apellido materno', validators=[DataRequired('Por favor introduzca el segundo apellido')])
    direccion = StringField(label='Dirección', validators=[DataRequired('Por favor introduzca la dirección')])
    telefono = StringField(label='Teléfono', validators=[DataRequired('Por favor introduzca el teléfono'), Length(min=10, max=10, message='Deben de ser 10 dígitos')])
    genero = SelectField(label='Género', choices=['Masculino', 'Femenino', 'Otro'])
    fecha_nacimiento = DateField(label='Fecha de nacimiento', validators=[DataRequired('Por favor introduzca la fecha de nacimiento')])
    puesto = StringField(label='Puesto', validators=[DataRequired('Por favor introduzca el puesto')])
    fecha_contratacion = DateField(label='Fecha de contratación', validators=[DataRequired('Por favor introduzca la fecha de contratación')])
    usuario = StringField(label='Usuario', validators=[DataRequired('Por favor introduzca el usuario')])
    password = PasswordField(label='Contraseña', validators=[DataRequired('Por favor introduzca la contraseña')])
    confirmar_password = PasswordField(label='Confirmar contraseña', validators=[DataRequired('Por favor confirme la contraseña'), EqualTo('password', message='Las contraseñas no coinciden')])
    submit = SubmitField(label='Guardar')

    def validate_usuario(self, usuario):
        user = mongo.db.empleados.find_one({'usuario.usuario': usuario.data});
        if user:
            raise ValidationError('El nombre de usuario ya existe. Ingrese otro diferente')

class RegistrarProductosForm(FlaskForm):
    nombre = StringField(label='Nombre', validators=[DataRequired('Por favor introduzca el nombre')])
    precio = DecimalField(label='Precio', validators=[DataRequired('Por favor introduzca el precio'), NumberRange(min=1, message='Introduzca un precio valido')])
    modelo = StringField(label='Modelo', validators=[DataRequired('Por favor introduzca el modelo')])
    marca = StringField(label='Marca', validators=[DataRequired('Por favor introduzca el marca')])
    descripcion = TextAreaField('Descripción', validators=[DataRequired('Por favor introduzca la descripción')])
    imagen = FileField('Foto')
    submit = SubmitField(label='Guardar')
