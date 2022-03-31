from flask import render_template, session, url_for, flash, redirect, request, jsonify, Response
from africa_botas import app, mongo, bcrypt
from africa_botas.forms import *
from africa_botas.helpers import login_required, get_empleado
from bson.objectid import ObjectId
from bson import json_util


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # form = PetForm()
    # pets = mongo.db.pets.find()
    # action = url_for('home')
    # if request.method == 'POST':
    #     if form.validate_on_submit():
    #         name = request.form.get('name')
    #         species = request.form.get('species')
    #         breed = request.form.get('breed')
    #         pet = {"name": name, "species": species, "breed": breed}
    #         mongo.db.pets.insert_one(pet)
    #         flash('The pet has been saved', 'success')
    #         return redirect(url_for('home'))
    # return render_template('index.html', form=form, pets=pets, action=action)
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
       


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            empleado = mongo.db.empleados.find_one({'usuario.usuario': form.usuario.data});
            if empleado:
                empleado['_id'] = str(empleado['_id'])
                print(empleado)
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
            empleado = get_empleado(form)
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            usuario = {
                'usuario': form.usuario.data,
                'password': hashed_password
            }
            empleado['usuario'] = usuario
            mongo.db.empleados.insert_one(empleado)
            flash('Empleado registrado exitosamente', 'success')
            return redirect(url_for('registrar_empleado'))
    return render_template('empleadosForm.html', titulo='Registrar empleado', form=form, operacion='Registrar')


@app.route('/empleado/detalle/<string:id>', methods=['GET', 'POST'])
@login_required
def modificar_empleado(id):
    form = DetalleEmpleadoForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            empleado = get_empleado(form)
            mongo.db.empleados.update_one({'_id': ObjectId(id)}, {'$set': empleado})
            flash('Empleado modificado exitosamente', 'success')
            return redirect(url_for('get_empleados'))
    empleado = mongo.db.empleados.find_one({"_id": ObjectId(id)})
    if empleado:
        form.nombre.data = empleado['persona']['nombre']
        form.apellido_p.data = empleado['persona']['apellido_p']
        form.apellido_m.data = empleado['persona']['apellido_m']
        form.direccion.data = empleado['persona']['direccion']
        form.telefono.data = empleado['persona']['telefono']
        form.genero.data = empleado['persona']['genero']
        form.fecha_nacimiento.data = empleado['fecha_nacimiento']
        form.puesto.data = empleado['puesto']
        form.fecha_contratacion.data = empleado['fecha_contratacion']
    return render_template('empleadosDetalle.html', titulo='Detalle empleado', form=form, operacion='Detalle')


@app.route('/empleado/borrar', methods=['POST'])
@login_required
def borrar_empleado():
    id = request.form.get('id')
    mongo.db.empleados.delete_one({"_id": ObjectId(id)})
    flash('Empleado eliminado exitosamente', 'danger')
    return redirect(url_for('get_empleados'))


@app.route('/empleado', methods=['POST', 'GET'])
@login_required
def get_empleados():
    form = BuscarEmpleadoForm()
    if request.method == 'POST':
        if form.busqueda.data:
            empleados = mongo.db.empleados.find({form.filtro.data: {'$regex': form.busqueda.data, '$options': 'i'}})
            return render_template('empleadosTable.html', titulo='Empleados', empleados=empleados, form=form)
    empleados = mongo.db.empleados.find()
    return render_template('empleadosTable.html', titulo='Empleados', empleados=empleados, form=form)


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


@app.route('/producto', methods=['POST', 'GET'])
@login_required
def get_productos():
    form = BuscarProductoForm()
    if request.method == 'POST':
        if form.busqueda.data:
            if form.filtro.data == 'precio':
                try:
                    productos = mongo.db.productos.find({'precio': float(form.busqueda.data)})
                except ValueError:
                    flash('Introduzca un valor numérico', 'warning')
                    productos = mongo.db.productos.find()
            else:
                productos = mongo.db.productos.find({form.filtro.data: {'$regex': form.busqueda.data, '$options': 'i'}})
            return render_template('productosTable.html', titulo='productos', productos=productos, form=form)
    productos = mongo.db.productos.find()
    return render_template('productosTable.html', titulo='Productos', productos=productos, form=form)


@app.route('/producto/detalle/<string:id>', methods=['POST', 'GET'])
@login_required
def modificar_producto(id):
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
            mongo.db.productos.update_one({'_id': ObjectId(id)},{'$set': producto})
            flash('Producto modificado exitosamente', 'success')
            return redirect(url_for('get_productos'))
    producto=mongo.db.productos.find_one({'_id': ObjectId(id)})
    if producto:
        form.nombre.data = producto["nombre"]
        form.precio.data = producto["precio"]
        form.marca.data = producto["marca"]
        form.modelo.data = producto["modelo"]
        form.descripcion.data = producto["descripcion"]
    return render_template('productosForm.html', titulo='Detalle productos', form=form, operacion='Detalle')


@app.route('/producto/borrar', methods=['POST'])
@login_required
def borrar_producto():
    id = request.form.get('id')
    mongo.db.productos.delete_one({"_id": ObjectId(id)})
    flash('Producto eliminado exitosamente', 'danger')
    return redirect(url_for('get_productos'))


@app.route('/misdatos', methods=['POST', 'GET'])
@login_required
def modificar_mis_datos():
    form = ModificarUsuario()
    empleado = session.get('empleado')
    id = str(empleado['_id'])
    if request.method == 'POST':
        if form.validate_on_submit():
            empleado.pop('_id')
            empleado['usuario']['usuario'] = form.usuario.data
            mongo.db.empleados.update_one({'_id': ObjectId(id)}, {'$set': empleado})
            empleado['_id'] = id
            flash('Usuario modificado exitosamente', 'success')
            return redirect(url_for('modificar_mis_datos'))
    form.usuario.data = empleado['usuario']['usuario']
    return render_template('verDatos.html', titulo='Mis datos', empleado=empleado, form=form)


@app.route('/cambiar-password', methods=['POST', 'GET'])
@login_required
def modificar_password():
    form = ModificarPassword()
    empleado = session.get('empleado')
    id = str(empleado['_id'])
    if request.method == 'POST':
        if form.validate_on_submit():
            empleado.pop('_id')
            hashed_password = bcrypt.generate_password_hash(form.password_nuevo.data).decode('utf-8')
            print(form.password_nuevo.data)
            print(hashed_password)
            empleado['usuario']['password'] = hashed_password
            mongo.db.empleados.update_one({'_id': ObjectId(id)}, {'$set': empleado})
            empleado['_id'] = id
            flash('Contraseña modificada exitosamente', 'success')
            return redirect(url_for('modificar_mis_datos'))
    return render_template('modificarPassword.html', titulo='Cambiar contraseña', form=form)


@app.route('/logout')
@login_required
def logout():
    session['empleado'] = None
    return redirect(url_for('login'))


@app.route('/login/movil', methods=['POST'])
def login_movil():
    usuario = request.form.get('usuario')
    password = request.form.get('password')
    empleado = mongo.db.empleados.find_one({'usuario.usuario': usuario})
    if empleado:
        empleado['_id'] = str(empleado['_id'])
        print(password)
        if bcrypt.check_password_hash(empleado['usuario']['password'], password):
            return jsonify({'code': 1, 'empleado': empleado})
        else:
            return jsonify({'code': 2, 'empleado': None})
    else:
        return jsonify({'code': 0, 'empleado': None})


@app.route('/productos/getAll')
def get_productos_movil():
    productos = mongo.db.productos.find()
    response = json_util.dumps(productos)
    return Response(response, mimetype="application/json")