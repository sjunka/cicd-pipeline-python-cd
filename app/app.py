# app/app.py
"""Aplicación web Flask de la calculadora."""

import os

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from .calculadora import sumar, restar, multiplicar, dividir, potencia, modulo

OPERACIONES = {
    "sumar": sumar,
    "restar": restar,
    "multiplicar": multiplicar,
    "dividir": dividir,
    "potencia": potencia,
    "modulo": modulo,
}

app = Flask(__name__)
# Clave aleatoria para firmar el token CSRF. En Docker, Gunicorn usa --preload
# para que todos los workers compartan esta misma clave.
app.config["SECRET_KEY"] = os.urandom(32)
csrf = CSRFProtect(app)


@app.route("/", methods=["GET", "POST"])
def index():
    """Muestra el formulario y, si llega un POST, calcula y muestra el resultado."""
    resultado = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operacion = request.form["operacion"]

            funcion = OPERACIONES.get(operacion)
            if funcion is None:
                resultado = "Operación no válida"
            else:
                resultado = funcion(num1, num2)
        except ValueError:
            resultado = "Error: Introduce números válidos"
        except ZeroDivisionError:
            resultado = "Error: No se puede dividir por cero"

    return render_template("index.html", resultado=resultado)


@app.route("/health")
def health():
    """Health check usado por el Load Balancer. Incluye la versión desplegada."""
    return {"status": "ok", "version": os.environ.get("APP_VERSION", "local")}


if __name__ == "__main__":  # pragma: no cover
    app.run(port=5000)
