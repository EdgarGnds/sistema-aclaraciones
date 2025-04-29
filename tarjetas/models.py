from database import db
from werkzeug.security import generate_password_hash
from datetime import datetime

class Tarjeta(db.Model):
    __tablename__ = 'tarjetas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(16), unique=True, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # débito/crédito
    estado = db.Column(db.String(20), nullable=False, default='activa')  # 👈 nuevo campo
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    
    cliente = db.relationship('Cliente', backref=db.backref('tarjetas', lazy=True))
    
    def __init__(self, numero, tipo, cliente_id):
        # En producción: self.numero = generate_password_hash(numero)
        self.numero = numero  # Para desarrollo/testing
        self.tipo = tipo
        self.estado = 'activa'  # 👈 se asigna como activa por default
        self.cliente_id = cliente_id
    
    @property
    def numero_enmascarado(self):
        """Devuelve: '•••• •••• •••• 1234'"""
        return f"•••• •••• •••• {self.numero[-4:]}" if self.numero else ""
    
    def __repr__(self):
        return f'<Tarjeta {self.tipo} {self.numero_enmascarado}>'

class HistorialCambioEstado(db.Model):
    __tablename__ = 'historial_cambios_estado'
    
    id = db.Column(db.Integer, primary_key=True)
    tarjeta_id = db.Column(db.Integer, db.ForeignKey('tarjetas.id'), nullable=False)
    estado_anterior = db.Column(db.String(20), nullable=False)
    estado_nuevo = db.Column(db.String(20), nullable=False)
    fecha_cambio = db.Column(db.DateTime, default=datetime.utcnow)
    realizado_por = db.Column(db.String(50), nullable=False)

    tarjeta = db.relationship('Tarjeta', backref='historial_estados')
