from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    usuario = StringField(label='Usuario', validators=[DataRequired('Por favor introduzca el usuario')])
    password = PasswordField(label='Contraseña', validators=[DataRequired('Por favor introduzca la contraseña')])
    recuerdame = BooleanField(label='Recueradme')
    submit = SubmitField(label='Iniciar Sesión')
