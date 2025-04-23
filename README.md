
# Sistema de Aclaraciones sobre Tarjetas

Este es un sistema en Python utilizando Flask, para la gestión de clientes, tarjetas y aclaraciones bancarias.

## Requisitos

- Python 3.8 o superior
- Virtualenv

## Instalación

```bash
python -m venv venv
source venv/Scripts/activate  # En Windows con Git Bash
pip install -r requirements.txt
python main.py
```

## Estructura

- `clientes/`, `tarjetas/`, `aclaraciones/`: Módulos con modelos, controladores y vistas.
- `notificaciones/`: Manejo de correos.
- `main.py`: Punto de entrada.
- `config.py`: Configuración.
- `database.py`: Conexión a base de datos.
