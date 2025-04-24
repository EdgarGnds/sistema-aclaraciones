from flask import Flask, render_template
from database import db
from clientes.views import clientes_bp
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

# 🔹 Ruta para probar el servidor
@app.route("/")
def home():
    return "Sistema de Aclaraciones funcionando 🚀"

# 🔹 Ruta para mostrar formulario web
@app.route("/registrar")
def formulario_cliente():
    return render_template("registro_cliente.html")

# 🔹 Rutas de cliente (API)
app.register_blueprint(clientes_bp)

# 🔹 Verificar la ruta de la base de datos
print("Ruta absoluta de la base de datos:", os.path.abspath('./data/aclaraciones.db'))

from clientes.models import Cliente  # 👈 Esto es lo que asegura que SQLAlchemy conozca el modelo

# 🔹 Crear tablas si no existen y arrancar el servidor
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos
    app.run(debug=True)
