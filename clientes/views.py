from flask import Blueprint, render_template, request, redirect, url_for, flash
from clientes.models import Cliente
from database import db

clientes_bp = Blueprint('clientes', __name__, template_folder='templates')

# Registro (Formulario + Procesamiento)
@clientes_bp.route('/registrar', methods=['GET', 'POST'])
def registrar_cliente():
    if request.method == 'POST':
        try:
            cliente = Cliente(
                nombre=request.form['nombre'],
                apellido=request.form['apellido'],
                correo=request.form['correo'],
                telefono=request.form['telefono']
            )
            db.session.add(cliente)
            db.session.commit()
            flash('✅ Cliente registrado exitosamente', 'success')
            return redirect(url_for('clientes.consultar_clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error: {str(e)}', 'danger')
    return render_template('clientes/registro.html')

# Consulta (Búsqueda + Listado)
@clientes_bp.route('/consultar', methods=['GET', 'POST'])
def consultar_clientes():
    clientes = Cliente.query
    if request.method == 'POST':
        busqueda = request.form.get('busqueda', '')
        clientes = clientes.filter(
            (Cliente.nombre.contains(busqueda)) |
            (Cliente.apellido.contains(busqueda)) |
            (Cliente.correo.contains(busqueda))
        )
    return render_template('clientes/consulta.html', clientes=clientes.all())

# Actualización (Edición)
@clientes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        try:
            cliente.nombre = request.form['nombre']
            cliente.apellido = request.form['apellido']
            cliente.correo = request.form['correo']
            cliente.telefono = request.form['telefono']
            db.session.commit()
            flash('✅ Cliente actualizado correctamente', 'success')
            return redirect(url_for('clientes.consultar_clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error: {str(e)}', 'danger')
    return render_template('clientes/editar.html', cliente=cliente)