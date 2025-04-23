
from flask import Flask
from database import db

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

@app.route("/")
def home():
    return "Sistema de Aclaraciones funcionando 🚀"

if __name__ == "__main__":
    app.run(debug=True)
