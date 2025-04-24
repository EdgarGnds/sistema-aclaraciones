from flask import Flask, render_template, redirect, url_for, flash
from database import db
from clientes.views import clientes_bp
from tarjetas.controllers import tarjetas as tarjetas_bp
import os
from dotenv import load_dotenv
import socket

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración
app.config.from_pyfile('config.py')
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Inicializar base de datos
db.init_app(app)

# Registrar Blueprints
app.register_blueprint(clientes_bp, url_prefix='/clientes')
app.register_blueprint(tarjetas_bp)

# Importar modelos para creación de tablas
from clientes.models import Cliente
from tarjetas.models import Tarjeta

# Función para obtener IP local (útil para acceso desde otros dispositivos)
def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))  # Usamos Google DNS como destino
            return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'  # Fallback si no se puede determinar la IP

# --------------------------
# Rutas principales
# --------------------------
@app.route('/')
def home():
    """Página principal del sistema"""
    return render_template('index.html')

@app.route('/about')
def about():
    """Página de información del sistema"""
    return render_template('about.html')

# --------------------------
# Manejo de errores
# --------------------------
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# --------------------------
# Inicialización
# --------------------------
def initialize_database():
    """Función para inicializar la base de datos"""
    with app.app_context():
        try:
            print("Creando tablas...")
            db.create_all()
            print(f"Ubicación de la BD: {os.path.abspath('./data/aclaraciones.db')}")
            
            # Mostrar URL de acceso (útil para conectar desde otros dispositivos)
            local_ip = get_local_ip()
            port = os.getenv('FLASK_PORT', '5000')
            print(f"\n🌐 Acceso desde red local: http://{local_ip}:{port}\n")
            
        except Exception as e:
            print(f"Error al crear tablas: {str(e)}")

if __name__ == "__main__":
    initialize_database()
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True') == 'True'
    )