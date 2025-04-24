from main import app  # En lugar de from app import app
from database import db
from clientes.models import Cliente  # 👈 IMPORTANTE

with app.app_context():
    db.create_all()  # Crear las tablas en la base de datos
