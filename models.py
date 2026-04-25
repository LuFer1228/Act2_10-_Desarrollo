# models.py

personajes = {}
contador_id = 1


def crear_personaje(datos):
    global contador_id

    personaje = {
        "id": contador_id,
        "nombre": datos["nombre"],
        "color_piel": datos["color_piel"],
        "raza": datos["raza"],
        "elemental": datos.get("elemental", "ninguno"),
        "fuerza": datos.get("fuerza", 10),
        "agilidad": datos.get("agilidad", 10),
        "magia": datos.get("magia", 10),
        "conocimiento": datos.get("conocimiento", 10),
    }

    personajes[contador_id] = personaje
    contador_id += 1
    return personaje


def obtener_todos():
    return list(personajes.values())


def obtener_por_id(pid):
    return personajes.get(pid)


def actualizar_personaje(pid, datos):
    if pid not in personajes:
        return None
    personaje = personajes[pid]
    for campo in ["nombre", "color_piel", "raza", "elemental", "fuerza", "agilidad", "magia", "conocimiento"]:
        if campo in datos:
            personaje[campo] = datos[campo]
    return personaje


def eliminar_personaje(pid):
    if pid in personajes:
        del personajes[pid]
        return True
    return False