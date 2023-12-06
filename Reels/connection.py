from pymongo import MongoClient

def conectar_bd():
    # Conexión a la base de datos MongoDB
    client = MongoClient("mongodb+srv://oscar:1234@cluster0.trndteq.mongodb.net/?")
    db = client["Dev"]
    colección = db.dev
    return colección
