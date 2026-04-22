import csv
import os

db_personajes = {}

def procesar_filas_recursivo(lector):
    try:
        fila = next(lector)
        nombre = fila.get("nombre", "Desconocido").strip()
        
        try:
            hp = int(fila.get("hp", 0))
            atq = int(fila.get("atq", 0))
            df = int(fila.get("def", 0))
        except ValueError:
            print(f"⚠️ Error en datos numéricos para {nombre}. Usando valores base.")
            hp, atq, df = 100, 10, 5

        # Asignación segura
        db_personajes[nombre] = {
            "hp": hp,
            "atq": atq,
            "def": df,
            "tipo": fila.get("tipo", "Ataque"),
            "img": fila.get("img", "default.png"),
            "sprite": fila.get("sprite", f"{nombre.lower()}_s.png") # Si no hay sprite, inventa uno
        }

        print(f"✅ {nombre} cargado correctamente.")
        procesar_filas_recursivo(lector)

    except StopIteration:
        return
    except Exception as e:
        print(f"❌ Error procesando fila: {e}")
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