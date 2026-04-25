# API REST - Gestión de Personajes RPG

API REST desarrollada con Python y Flask para gestionar personajes de un juego de rol y simular batallas entre ellos.

## Tecnologias Utilizadas
- Python
- Flask

## Instalación y ejecucion del codigo

### 1. Clonar el repositorio
```bash
git clone https://github.com/LuFer1228/Act2_10-_Desarrollo.git
cd Act2_10-_Desarrollo
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Correr el servidor
```bash
python app.py
```
El servidor quedará corriendo en `http://127.0.0.1:5000`

## Endpoints

### Personajes
Metodo - Ruta - ¿Que hace?
POST = `/personajes` = Crea nuevos personajes
GET= `/personajes` = Listar todos los personajes existentes
GET=  `/personajes/<id>` =Consulta el personaje por ID
PUT= `/personajes/<id>` = Actualiza la informacion del personaje
DELETE= `/personajes/<id>`= Elimina personajes por ID

### Batallas
Metodo - Ruta - ¿Que hace?
POST = `/batalla` = Simular batalla |

## Ejemplos de uso

### Crear personaje
POST `http://127.0.0.1:5000/personajes`
json
{
 "nombre": "Ifrit",
  "color_piel": "rojizo",
  "raza": "demonio",
  "elemental": "fuego",
  "fuerza": 80,
  "agilidad": 60,
  "magia": 70,
  "conocimiento": 65
}


### Simular batalla
POST `http://127.0.0.1:5000/batalla`
json
{
  "id1": 1,
  "id2": 2
}

### Ejemplo de respuesta de batalla
json
{
   "ganador": "Ifrit",
  "resumen": "Ifrit domina la batalla con su estrategia superior.",
  "elemental": {
    "Ifrit": "🔥 Ifrit tiene ventaja elemental (fuego) → x1.5 de fuerza",
    "Sylph": "💀 Sylph tiene desventaja elemental (aire) → x0.75 de fuerza"
  },
  "puntajes": {
    "Ifrit": 310.5,
    "Sylph": 280.3
  }
}

## Sistema Elemental

Cada personaje puede tener un elemento que influye en la batalla:

Fuego > Aire > Agua 
Aire > Agua > Fuego 
Agua > Fuego > Aire 

- Ventaja elemental = x1.5 de fuerza
- Desventaja elemental = x0.75 de fuerza
- Sin ventaja = x1.0 (neutro)


## Lógica de combate
Cada estadística tiene un peso diferente en la batalla:
- Fuerza x1.5 — daño físico
- Magia x1.2 — ataque especial con aleatoriedad
- Conocimiento x1.0 — bonus estratégico
- Agilidad x0.8 — evasión
