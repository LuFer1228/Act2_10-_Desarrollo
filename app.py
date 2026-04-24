# app.py

from flask import Flask
from routes.personajes import personajes_bp
from routes.batallas import batallas_bp

app = Flask(__name__)

# Registrar los blueprints
app.register_blueprint(personajes_bp)
app.register_blueprint(batallas_bp)

if __name__ == "__main__":
    app.run(debug=True)