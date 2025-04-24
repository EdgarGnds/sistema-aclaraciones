from flask import Blueprint, request
from clientes.controllers import crear_cliente

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['POST'])
def registrar_cliente():
    data = request.get_json()
    return crear_cliente(data)