# utils.py
def load_user(username):
# Simulation d'un stockage utilisateur non sécurisé (ex: base
fictive)
fake_db = {"admin": "admin123", "user": "pass"}
return fake_db.get(username)