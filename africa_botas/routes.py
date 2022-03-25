from flask import render_template, session, url_for, flash, redirect, request, jsonify
from datetime import datetime
from africa_botas import app, mongo, bcrypt
from africa_botas.forms import LoginForm, RegistrarEmpleadoForm, RegistrarProductosForm
from africa_botas.helpers import login_required
from bson.objectid import ObjectId


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('dashboard.html', titulo='dashboard', empleado = session.get('empleado'))

@app.route('/modify/<string:id>', methods=['GET', 'POST'])
def modify(id):
    pass
    # form = PetForm()
    # pet = mongo.db.pets.find_one({"_id": ObjectId(id)})
    # pets = mongo.db.pets.find()
    # action = url_for('modify', id=id)
    # if request.method == 'POST':
    #     if form.validate_on_submit():
    #         name = request.form.get('name')
    #         species = request.form.get('species')
    #         breed = request.form.get('breed')
    #         pet = {"name": name, "species": species, "breed": breed}
    #         mongo.db.pets.update_one({"_id": ObjectId(id)}, {"$set": pet})
    #         flash('The pet has been modified', 'warning')
    #         return redirect(url_for('home'))
    # form.name.data = pet['name']
    # form.species.data = pet['species']
    # form.breed.data = pet['breed']
    # return render_template('index.html', form=form, pets=pets, action=action)
       
       
@app.route('/delete', methods=['POST'])
def delete():
    # id = request.form.get('id')
    # mongo.db.pets.delete_one({"_id": ObjectId(id)})
    # flash('The pet has been deleted', 'danger')
    # return redirect(url_for('home'))
    pass

@app.route('/search', methods=['GET'])
def search():
    
    pass

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            empleado = mongo.db.empleados.find_one({'usuario.usuario': form.usuario.data});
            if empleado:
                empleado['_id'] = str(empleado['_id'])
                # usuario = empleado.get('usuario')
                if bcrypt.check_password_hash(empleado['usuario']['password'] , form.password.data):
                    session['empleado'] = empleado
                    return redirect(url_for('home'))
                else:
                    flash('La contraseña es errónea', 'danger')
            else:
                flash(f'El usuario {form.usuario.data} no existe', 'danger')
    return render_template('login.html', titulo='Iniciar sesión', form=form)


@app.route('/empleado/registrar', methods=['POST', 'GET'])
@login_required
def registrar_empleado():
    form = RegistrarEmpleadoForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            persona = {
                'nombre': form.nombre.data,
                'apellido_p': form.apellido_p.data,
                'apellido_m': form.apellido_m.data,
                'direccion': form.direccion.data,
                'telefono': form.telefono.data,
                'genero': form.genero.data
            }
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            usuario = {
                'usuario': form.usuario.data,
                'password': hashed_password
            }
            fecha_contratacion = form.fecha_contratacion.data
            fecha_nacimiento = form.fecha_nacimiento.data
            empleado = {
                'puesto': form.puesto.data,
                'fecha_contratacion': datetime(fecha_contratacion.year, fecha_contratacion.month, fecha_contratacion.day),
                'fecha_nacimiento': datetime(fecha_nacimiento.year, fecha_nacimiento.month, fecha_nacimiento.day),
                'persona': persona,
                'usuario': usuario
            }
            mongo.db.empleados.insert_one(empleado)
            flash('Empleado registrado exitosamente', 'success')
    return render_template('empleadosForm.html', titulo='Registrar empleado', form=form, operacion='Registrar')

@app.route('/empleado')
@login_required
def get_empleados():
    empleados = mongo.db.empleados.find()
    return render_template('empleadosTable.html', titulo='Empleados', empleados=empleados)


@app.route('/producto/registrar', methods=['POST', 'GET'])
@login_required
def registrar_producto():
    form = RegistrarProductosForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            producto = {
                'nombre': form.nombre.data,
                'precio': float(form.precio.data),
                'marca': form.marca.data,
                'modelo': form.modelo.data,
                'descripcion': form.descripcion.data
            }
            mongo.db.productos.insert_one(producto)
            flash('Producto registrado exitosamente', 'success')
    return render_template('productosForm.html', titulo='Registrar productos', form=form, operacion='Registrar')

@app.route('/producto')
@login_required
def get_productos():
    productos = mongo.db.productos.find()
    return render_template('productosTable.html', titulo='Productos', productos=productos)
