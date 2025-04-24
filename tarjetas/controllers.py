from flask import Blueprint, render_template, request, redirect, url_for, flash
from tarjetas.models import Tarjeta
from clientes.models import Cliente
from database import db

tarjetas = Blueprint('tarjetas', __name__)

@tarjetas.route('/tarjetas', methods=['GET'])
def formulario_tarjeta():
    clientes = Cliente.query.all()
    return render_template('tarjetas/registro_tarjeta.html', clientes=clientes)

@tarjetas.route('/tarjetas', methods=['POST'])
def registrar_tarjeta():
    try:
        # Limpia y valida el número (16 dígitos sin espacios)
        numero = request.form['numero'].replace(" ", "")
        
        if len(numero) != 16 or not numero.isdigit():
            flash('❌ El número debe tener 16 dígitos', 'danger')
            return redirect(url_for('tarjetas.formulario_tarjeta'))
            
        nueva_tarjeta = Tarjeta(
            numero=numero[:16],  # Asegura máximo 16 caracteres
            tipo=request.form['tipo'],
            cliente_id=request.form['cliente_id']
        )
        
        db.session.add(nueva_tarjeta)
        db.session.commit()
        flash('✅ Tarjeta registrada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error: {e}', 'danger')
    
    return redirect(url_for('tarjetas.formulario_tarjeta'))

@tarjetas.route('/tarjetas/lista')
def lista_tarjetas():
    # Consulta optimizada con join para evitar N+1
    tarjetas = db.session.query(Tarjeta).join(Cliente).options(
        db.contains_eager(Tarjeta.cliente)
    ).order_by(Cliente.nombre).all()
    
    return render_template('tarjetas/lista_tarjetas.html', 
                         tarjetas=tarjetas)
