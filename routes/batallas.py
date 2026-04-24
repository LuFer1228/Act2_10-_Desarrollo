# routes/batallas.py

from flask import Blueprint, request, jsonify
import models
import random

batallas_bp = Blueprint("batallas", __name__)


def calcular_poder(p):
    golpe_fisico = p["fuerza"] * 1.5
    evasion = p["agilidad"] * 0.8
    ataque_magico = p["magia"] * 1.2 + random.uniform(0, p["magia"] * 0.3)
    bonus_estrategia = p["conocimiento"] * 1.0

    poder_total = golpe_fisico + evasion + ataque_magico + bonus_estrategia
    return round(poder_total, 2)


# POST /batalla — Simular batalla
@batallas_bp.route("/batalla", methods=["POST"])
def batalla():
    datos = request.get_json()

    if "id1" not in datos or "id2" not in datos:
        return jsonify({"error": "Debes enviar 'id1' e 'id2'"}), 400

    p1 = models.obtener_por_id(datos["id1"])
    p2 = models.obtener_por_id(datos["id2"])

    if not p1:
        return jsonify({"error": f"Personaje con id {datos['id1']} no encontrado"}), 404
    if not p2:
        return jsonify({"error": f"Personaje con id {datos['id2']} no encontrado"}), 404

    poder1 = calcular_poder(p1)
    poder2 = calcular_poder(p2)

    if poder1 > poder2:
        ganador = p1["nombre"]
        resultado = f"{p1['nombre']} domina la batalla con su estrategia superior."
    elif poder2 > poder1:
        ganador = p2["nombre"]
        resultado = f"{p2['nombre']} triunfa con una combinación devastadora de habilidades."
    else:
        ganador = "Empate"
        resultado = "¡Los dos guerreros están perfectamente igualados!"

    return jsonify({
        "ganador": ganador,
        "resumen": resultado,
        "puntajes": {
            p1["nombre"]: poder1,
            p2["nombre"]: poder2
        },
        "detalle": {
            p1["nombre"]: {
                "fuerza": p1["fuerza"],
                "agilidad": p1["agilidad"],
                "magia": p1["magia"],
                "conocimiento": p1["conocimiento"]
            },
            p2["nombre"]: {
                "fuerza": p2["fuerza"],
                "agilidad": p2["agilidad"],
                "magia": p2["magia"],
                "conocimiento": p2["conocimiento"]
            }
        }
    }), 200