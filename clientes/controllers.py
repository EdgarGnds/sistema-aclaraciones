from clientes.models import Cliente
from database import db
from flask import jsonify

def crear_cliente(data):
    # Validar si ya existe el correo o teléfono
    if Cliente.query.filter_by(correo=data['correo']).first():
        return jsonify({"error": "El correo ya está registrado."}), 400
    if Cliente.query.filter_by(telefono=data['telefono']).first():
        return jsonify({"error": "El teléfono ya está registrado."}), 400

    cliente = Cliente(
        nombre=data['nombre'],
        apellido=data['apellido'],
        correo=data['correo'],
        telefono=data['telefono']
    )
    db.session.add(cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente registrado exitosamente."}), 201