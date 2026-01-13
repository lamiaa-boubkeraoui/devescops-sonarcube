from flask import Flask, request, escape
import hashlib
import subprocess
import os

app = Flask(__name__)

# Mot de passe récupéré uniquement depuis une variable d’environnement
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

if ADMIN_PASSWORD is None:
    raise RuntimeError("La variable d'environnement ADMIN_PASSWORD doit être définie")

# Cryptographie forte (SHA-256)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing credentials", 400

    # Authentification plus sûre
    if (
        username == "admin"
        and hash_password(password) == hash_password(ADMIN_PASSWORD)
    ):
        return "Logged in", 200

    return "Invalid credentials", 401


@app.route("/ping", methods=["GET"])
def ping():
    host = request.args.get("host", "localhost")

    # Validation simple de l'entrée
    if not host.replace(".", "").isalnum():
        return "Invalid host", 400

    # Suppression de shell=True (anti-injection)
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True,
        check=False
    )

    return result.stdout


@app.route("/hello", methods=["GET"])
def hello():
    name = request.args.get("name", "user")

    # Protection contre XSS
    safe_name = escape(name)

    return f"<h1>Hello {safe_name}</h1>"


if __name__ == "__main__":
    # Debug désactivé (sécurité)
    app.run(debug=False)
