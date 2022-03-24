from crypt import methods
from flask import render_template, session, url_for, flash, redirect, request, Response
from datetime import datetime
from africa_botas import app, mongo, bcrypt
from africa_botas.forms import LoginForm, RegistrarEmpleadoForm
from africa_botas.helpers import login_required
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
       
       
@app.route('/delete', methods=['POST'])
def delete():
    # id = request.form.get('id')
    # mongo.db.pets.delete_one({"_id": ObjectId(id)})
    # flash('The pet has been deleted', 'danger')
    # return redirect(url_for('home'))
    pass


@app.route('/login', methods=['POST'])
def login():
    usuario = request.json['usuario']
    password = request.json['password']
    
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

@app.route('/empleados/get')
# @login_required
def get_empleados():
    empleados = mongo.db.empleados.find()
    response = json_util.dumps(empleados)
    return Response(response, mimetype='application/json')
