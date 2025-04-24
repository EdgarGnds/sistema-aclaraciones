from main import app
from database import db
from clientes.models import Cliente  # Asegúrate de tener el modelo definido

# Mostrar la ruta de la base de datos
print("Creando base de datos en:", app.config["SQLALCHEMY_DATABASE_URI"])

# Crear la base de datos
with app.app_context():
    db.create_all()
    print("✅ Base de datos creada correctamente.")
