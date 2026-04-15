# logica.py
from Logic.datos import db_personajes

estado_juego = {
    "nombre": False,
    "personaje": False,
    "avatar": False,
    "stats": None
}

def validar_nombre(nombre):
    return len(nombre.strip()) >= 3

def obtener_stats(nombre_pj):
    return db_personajes.get(nombre_pj)