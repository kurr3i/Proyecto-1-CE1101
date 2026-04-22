from Logic.datos import db_personajes

estado_juego = {
    "nombre": False,
    "personajes_elegidos": [],
    "avatar": False,
    "avatar_icono": None,
    "progreso": 0,
    "puntos": 0,
    "nivel_actual": 1 
}

def validar_nombre_recursivo(nombre):
    if not nombre:
        return False
    if nombre[0] != " ":
        return len(nombre) >= 3
    return validar_nombre_recursivo(nombre[1:])

def validar_nombre(nombre):
    return validar_nombre_recursivo(nombre)

def buscar_stats_recursivo(nombres_db, objetivo):
    if not nombres_db:
        return None
    if nombres_db[0] == objetivo:
        return db_personajes[objetivo]
    return buscar_stats_recursivo(nombres_db[1:], objetivo)

def obtener_stats(nombre_pj):
    return buscar_stats_recursivo(list(db_personajes.keys()), nombre_pj)

def asignar_avatar(icono):
    estado_juego["avatar"] = True
    estado_juego["avatar_icono"] = icono

def registrar_victoria_nivel():
    """
    Sube el nivel actual. Si se pasa del límite (ej. nivel 3),
    cambia el estado a 'VICTORIA'.
    """
    LIMITE_NIVELES = 5
    
    if estado_juego["nivel_actual"] < LIMITE_NIVELES:
        estado_juego["nivel_actual"] += 1
        print(f"✅ Nivel superado. Siguiente nivel: {estado_juego['nivel_actual']}")
    else:
        estado_juego["nivel_actual"] = "VICTORIA"
        print("🏆 ¡JUEGO COMPLETADO! Estado: VICTORIA")