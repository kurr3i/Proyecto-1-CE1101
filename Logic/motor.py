# logica.py
from Logic.datos import db_personajes

estado_juego = {
    "nombre": False,
    "personajes_elegidos": [],
    "avatar": False,
    "progreso": 0,
    "puntos": 0  
}

def validar_nombre(nombre):
    return len(nombre.strip()) >= 3

def obtener_stats(nombre_pj):
    return db_personajes.get(nombre_pj)

def asignar_avatar(icono):
    estado_juego["avatar"] = True
    estado_juego["avatar_icono"] = icono