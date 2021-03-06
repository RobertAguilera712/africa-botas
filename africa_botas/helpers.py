from flask import redirect, session
from datetime import datetime
from functools import wraps
from africa_botas import bcrypt, app
import secrets, os


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("empleado") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_empleado(form):
    persona = {
        'nombre': form.nombre.data,
        'apellido_p': form.apellido_p.data,
        'apellido_m': form.apellido_m.data,
        'direccion': form.direccion.data,
        'telefono': form.telefono.data,
        'genero': form.genero.data
    }
    fecha_contratacion = form.fecha_contratacion.data
    fecha_nacimiento = form.fecha_nacimiento.data
    empleado = {
        'puesto': form.puesto.data,
        'fecha_contratacion': datetime(fecha_contratacion.year, fecha_contratacion.month, fecha_contratacion.day),
        'fecha_nacimiento': datetime(fecha_nacimiento.year, fecha_nacimiento.month, fecha_nacimiento.day),
        'persona': persona
    }
    return empleado


def guardar_foto(foto):
    random_hex = secrets.token_hex(8)
    _, extension = os.path.splitext(foto.filename)
    nombre_imagen = random_hex + extension
    ruta_imagen = os.path.join(app.root_path, 'static/img-productos', nombre_imagen)
    foto.save(ruta_imagen)
    return nombre_imagen

