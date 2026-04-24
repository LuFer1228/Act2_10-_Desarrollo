# routes/personajes.py
from flask import Blueprint, request, jsonify
import models

personajes_bp = Blueprint("personajes", __name__)


# POST /personajes — Crear personaje
@personajes_bp.route("/personajes", methods=["POST"])
def crear():
    datos = request.get_json()

    campos_requeridos = ["nombre", "color_piel", "raza"]
    for campo in campos_requeridos:
        if campo not in datos:
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    personaje = models.crear_personaje(datos)
    return jsonify(personaje), 201


# GET /personajes — Listar todos
@personajes_bp.route("/personajes", methods=["GET"])
def listar():
    return jsonify(models.obtener_todos()), 200


# GET /personajes/<id> — Consultar por ID
@personajes_bp.route("/personajes/<int:pid>", methods=["GET"])
def obtener(pid):
    personaje = models.obtener_por_id(pid)
    if not personaje:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(personaje), 200


# PUT /personajes/<id> — Actualizar
@personajes_bp.route("/personajes/<int:pid>", methods=["PUT"])
def actualizar(pid):
    datos = request.get_json()
    personaje = models.actualizar_personaje(pid, datos)
    if not personaje:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(personaje), 200


# DELETE /personajes/<id> — Eliminar
@personajes_bp.route("/personajes/<int:pid>", methods=["DELETE"])
def eliminar(pid):
    eliminado = models.eliminar_personaje(pid)
    if not eliminado:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify({"mensaje": "Personaje eliminado correctamente"}), 200