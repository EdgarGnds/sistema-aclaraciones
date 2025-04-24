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

def buscar_clientes(criterio):
    query = Cliente.query
    if "nombre" in criterio:
        query = query.filter(Cliente.nombre.like(f"%{criterio['nombre']}%"))
    if "correo" in criterio:
        query = query.filter(Cliente.correo.like(f"%{criterio['correo']}%"))
    if "telefono" in criterio:
        query = query.filter(Cliente.telefono.like(f"%{criterio['telefono']}%"))
    
    clientes = query.all()
    resultados = [
        {
            "id": c.id,
            "nombre": c.nombre,
            "apellido": c.apellido,
            "correo": c.correo,
            "telefono": c.telefono
        }
        for c in clientes
    ]
    return jsonify(resultados), 200

def actualizar_cliente(cliente_id, nuevos_datos):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    # Validar que no se repitan correos o teléfonos de otros clientes
    if 'correo' in nuevos_datos:
        existente = Cliente.query.filter(Cliente.correo == nuevos_datos['correo'], Cliente.id != cliente_id).first()
        if existente:
            return jsonify({"error": "Ese correo ya está en uso por otro cliente"}), 400
        cliente.correo = nuevos_datos['correo']

    if 'telefono' in nuevos_datos:
        existente = Cliente.query.filter(Cliente.telefono == nuevos_datos['telefono'], Cliente.id != cliente_id).first()
        if existente:
            return jsonify({"error": "Ese teléfono ya está en uso por otro cliente"}), 400
        cliente.telefono = nuevos_datos['telefono']

    cliente.nombre = nuevos_datos.get('nombre', cliente.nombre)
    cliente.apellido = nuevos_datos.get('apellido', cliente.apellido)

    db.session.commit()
    return jsonify({"mensaje": "Cliente actualizado correctamente"}), 200