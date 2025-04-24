from flask import Blueprint, request, jsonify, render_template
from clientes.controllers import crear_cliente, buscar_clientes, actualizar_cliente

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['POST'])
def registrar_cliente():
    data = request.get_json()
    return crear_cliente(data)

@clientes_bp.route('/clientes/buscar', methods=['GET'])
def buscar():
    criterio = request.args.to_dict()
    return buscar_clientes(criterio)

@clientes_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def editar_cliente(cliente_id):
    nuevos_datos = request.get_json()
    return actualizar_cliente(cliente_id, nuevos_datos)

@clientes_bp.route('/clientes/consulta', methods=['GET'])
def vista_consulta():
    return render_template('clientes/consulta.html')
