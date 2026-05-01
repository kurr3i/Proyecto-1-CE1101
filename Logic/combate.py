import random
from Logic.datos import db_personajes

def buscar_nombre_db_recursivo(claves, objetivo):
    if not claves:
        return None
    actual = claves[0]
    if limpiar_nombre_recursivo(actual).lower() == limpiar_nombre_recursivo(objetivo).lower():
        return actual
    return buscar_nombre_db_recursivo(claves[1:], objetivo)

def limpiar_nombre_recursivo(nombre):
    if not nombre:
        return ""
    if nombre[0] == " ":
        return limpiar_nombre_recursivo(nombre[1:])
    if nombre[-1] == " ":
        return limpiar_nombre_recursivo(nombre[:-1])
    return nombre

def calcular_danio(atq_atacante, def_defensor):
    """Retorna el daño calculado y un booleano que indica si fue golpe crítico."""
    danio_base = atq_atacante - def_defensor
    if danio_base <= 0:
        danio_base = 1
        
    # 20% de probabilidad de golpe crítico
    es_critico = random.randint(1, 100) <= 20
    
    if es_critico:
        danio_final = danio_base * 2
        print(f"💥 ¡GOLPE CRÍTICO! Daño duplicado: {danio_final}")
    else:
        danio_final = danio_base
        
    return danio_final, es_critico

def obtener_nombre_pj(pj):
    if not pj: return None
    return pj.get("nombre") or pj.get("name") or pj.get("Nombre")

def procesar_ataque_recursivo(estado, es_jugador):
    """
    Maneja el ataque y retorna (KO, Daño, Es_Critico).
    """
    atacante = estado["activo_jugador"] if es_jugador else estado["activo_hollow"]
    defensor = estado["activo_hollow"] if es_jugador else estado["activo_jugador"]

    danio, es_critico = calcular_danio(atacante["atq"], defensor["def"])
    defensor["hp"] -= danio
    
    return defensor["hp"] <= 0, danio, es_critico

def gestionar_captura(estado, victima_es_jugador):
    equipo_pierde = estado["equipo_jugador"] if victima_es_jugador else estado["equipo_hollow"]
    equipo_gana = estado["equipo_hollow"] if victima_es_jugador else estado["equipo_jugador"]
    pj = estado["activo_jugador"] if victima_es_jugador else estado["activo_hollow"]

    if pj in equipo_pierde:
        equipo_pierde.remove(pj)
    
    nombre_real = obtener_nombre_pj(pj)
    
    if nombre_real in db_personajes:
        pj["hp"] = db_personajes[nombre_real]["hp"]
        equipo_gana.append(pj)
    
    if not victima_es_jugador:
        estado["puntos_jugador"] = estado.get("puntos_jugador", 0) + 1

def crear_equipo_hollow_recursivo(nombres, cantidad):
    if cantidad == 0 or not nombres:
        return []
    
    seleccion = random.choice(nombres)
    restantes = [n for n in nombres if n != seleccion]
    
    d = db_personajes[seleccion]
    pj = {
        "nombre": seleccion,
        "hp": d["hp"],
        "atq": d["atq"],
        "def": d["def"],
        "img": d["img"],
        "sprite": d.get("sprite", f"{seleccion.lower()}_s.png")
    }
    
    return [pj] + crear_equipo_hollow_recursivo(restantes, cantidad - 1)

def construir_equipo_jugador_recursivo(lista):
    if not lista:
        return []
    
    elemento = lista[0]
    nombre = obtener_nombre_pj(elemento) if isinstance(elemento, dict) else elemento
    nombre_real = buscar_nombre_db_recursivo(list(db_personajes.keys()), nombre)
    stats = db_personajes.get(nombre_real, {})

    pj = {
        "nombre": nombre_real if nombre_real else "Desconocido",
        "hp": stats.get("hp", 100),
        "atq": stats.get("atq", 50),
        "def": stats.get("def", 50),
        "img": stats.get("img", ""),
        "sprite": stats.get("sprite", f"{nombre_real.lower()}_s.png" if nombre_real else "default_s.png")
    }

    return [pj] + construir_equipo_jugador_recursivo(lista[1:])

def inicializar_batalla(equipo_jugador):
    equipo_jugador_objs = construir_equipo_jugador_recursivo(equipo_jugador)
    
    # Lista limpia, sin filtros
    nombres_permitidos = list(db_personajes.keys())
    
    equipo_hollow = crear_equipo_hollow_recursivo(nombres_permitidos, 3)

    return {
        "equipo_jugador": equipo_jugador_objs,
        "equipo_hollow": equipo_hollow,
        "activo_jugador": None,
        "activo_hollow": equipo_hollow[0] if equipo_hollow else None,
        "puntos_jugador": 0
    }