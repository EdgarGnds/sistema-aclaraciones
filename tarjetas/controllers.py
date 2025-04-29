from flask import Blueprint, render_template, request, redirect, url_for, flash
from tarjetas.models import Tarjeta, HistorialCambioEstado  # <- Importamos Historial
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
    
    return render_template('tarjetas/lista_tarjetas.html', tarjetas=tarjetas)

@tarjetas.route('/tarjetas/cambiar_estado/<int:tarjeta_id>', methods=['POST'])
def cambiar_estado_tarjeta(tarjeta_id):
    nuevo_estado = request.form.get('nuevo_estado')
    tarjeta = Tarjeta.query.get_or_404(tarjeta_id)

    if nuevo_estado not in ['activa', 'bloqueada', 'cancelada']:
        flash('❌ Estado inválido', 'danger')
        return redirect(url_for('tarjetas.lista_tarjetas'))

    try:
        # Guardar el estado ANTES de cambiarlo
        estado_anterior = tarjeta.estado
        
        # Actualizar el estado
        tarjeta.estado = nuevo_estado
        
        # Registrar en historial (con todos los campos requeridos)
        historial = HistorialCambioEstado(
            tarjeta_id=tarjeta.id,
            estado_anterior=estado_anterior,  # <-- Ahora tiene valor
            estado_nuevo=nuevo_estado,
            realizado_por="admin"  # <-- Reemplazar con sistema de autenticación
            # fecha_cambio se asigna automáticamente por el default
        )
        
        db.session.add(historial)
        db.session.commit()
        
        flash(f'✅ Estado actualizado a "{nuevo_estado.capitalize()}"', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error: {str(e)}', 'danger')
    
    return redirect(url_for('tarjetas.lista_tarjetas'))

@tarjetas.route('/tarjetas/historial')
def historial_tarjetas():
    historial = db.session.query(HistorialCambioEstado).join(Tarjeta).options(
        db.contains_eager(HistorialCambioEstado.tarjeta)
    ).order_by(HistorialCambioEstado.fecha_cambio.desc()).all()
    
    return render_template('tarjetas/historial.html', historial=historial)

