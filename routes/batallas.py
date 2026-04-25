# routes/batallas.py

from flask import Blueprint, request, jsonify
import models
import random

batallas_bp = Blueprint("batallas", __name__)

# Tabla de ventajas elementales
# clave: elemento atacante → valor: elemento al que le gana
VENTAJAS = {
    "fuego": "aire",
    "aire": "agua",
    "agua": "fuego"
}


def get_ventaja_elemental(atacante, defensor):
    """
    Retorna 1.5 si el atacante tiene ventaja elemental,
    0.75 si tiene desventaja, o 1.0 si es neutro.
    """
    if atacante not in VENTAJAS:
        return 1.0, "neutro"
    
    if VENTAJAS[atacante] == defensor:
        return 1.5, "ventaja"
    elif VENTAJAS.get(defensor) == atacante:
        return 0.75, "desventaja"
    else:
        return 1.0, "neutro"


def calcular_poder(p, multiplicador_elemental=1.0):
    """
    Fórmula de poder con multiplicador elemental aplicado a la fuerza.
    """
    golpe_fisico = p["fuerza"] * 1.5 * multiplicador_elemental  # ← elemental afecta la fuerza
    evasion = p["agilidad"] * 0.8
    ataque_magico = p["magia"] * 1.2 + random.uniform(0, p["magia"] * 0.3)
    bonus_estrategia = p["conocimiento"] * 1.0

    poder_total = golpe_fisico + evasion + ataque_magico + bonus_estrategia
    return round(poder_total, 2)


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

    # Calcular ventajas elementales
    elem1 = p1.get("elemental", "ninguno")
    elem2 = p2.get("elemental", "ninguno")

    mult1, estado1 = get_ventaja_elemental(elem1, elem2)
    mult2, estado2 = get_ventaja_elemental(elem2, elem1)

    # Calcular poder con multiplicador elemental
    poder1 = calcular_poder(p1, mult1)
    poder2 = calcular_poder(p2, mult2)

    # Mensaje elemental
    def mensaje_elemental(nombre, elemento, estado):
        if estado == "ventaja":
            return f"🔥 {nombre} tiene ventaja elemental ({elemento}) → x1.5 de fuerza"
        elif estado == "desventaja":
            return f"💀 {nombre} tiene desventaja elemental ({elemento}) → x0.75 de fuerza"
        else:
            return f"⚪ {nombre} no tiene ventaja elemental ({elemento})"

    # Determinar ganador
    if poder1 > poder2:
        ganador = p1["nombre"]
        resumen = f"{p1['nombre']} Flawless Victory. Fatality."
    elif poder2 > poder1:
        ganador = p2["nombre"]
        resumen = f"{p2['nombre']} Mission Passed! Respect +1000."
    else:
        ganador = "Empate"
        resumen = "Draw. No winners, no losers. Solo otra batalla pendiente."

    return jsonify({
        "ganador": ganador,
        "resumen": resumen,
        "elemental": {
            p1["nombre"]: mensaje_elemental(p1["nombre"], elem1, estado1),
            p2["nombre"]: mensaje_elemental(p2["nombre"], elem2, estado2)
        },
        "puntajes": {
            p1["nombre"]: poder1,
            p2["nombre"]: poder2
        },
        "detalle": {
            p1["nombre"]: {
                "elemental": elem1,
                "fuerza": p1["fuerza"],
                "agilidad": p1["agilidad"],
                "magia": p1["magia"],
                "conocimiento": p1["conocimiento"]
            },
            p2["nombre"]: {
                "elemental": elem2,
                "fuerza": p2["fuerza"],
                "agilidad": p2["agilidad"],
                "magia": p2["magia"],
                "conocimiento": p2["conocimiento"]
            }
        }
    }), 200