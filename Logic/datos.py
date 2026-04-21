import csv
import os

db_personajes = {}

def procesar_filas_recursivo(lector):
    try:
        fila = next(lector)
        db_personajes[fila["nombre"]] = {
            "hp": int(fila["hp"]),
            "atq": int(fila["atq"]),
            "def": int(fila["def"]),
            "tipo": fila["tipo"],
            "img": fila["img"]
        }
        procesar_filas_recursivo(lector)
    except StopIteration:
        return

def cargar_personajes():
    global db_personajes
    ruta = os.path.join(os.path.dirname(__file__), "personajes.csv")
    try:
        with open(ruta, mode='r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            procesar_filas_recursivo(lector)
        print("✅ Personajes migrados recursivamente desde CSV.")
    except Exception as e:
        print(f"❌ Error migrando personajes: {e}")

cargar_personajes()

lista_avatares = [
    {"nombre": "L (Death Note)", "img": "l_deathnote.png"},
    {"nombre": "Franz Kafka", "img": "franz_kafka.png"},
    {"nombre": "Ilia Topuria", "img": "ilia_topuria.png"}
]

tierras_hollows = [
    "Planeta Radiator (🏁)", "Planeta Pride (🦁)", 
    "Planeta Monstro (👁️)", "Planeta Shrek (🧅)", 
    "Planeta Zootopia (🦊)"
]

coordenadas_tierras = [
    (150, 600), (350, 400), (512, 200), (700, 450), (900, 650)
]