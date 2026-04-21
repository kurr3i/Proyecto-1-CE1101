import tkinter as tk
import os

def buscar_ruta_recursiva(intentos, nombre):
    if not intentos:
        return None
    
    ruta_actual = os.path.join(intentos[0], "Assets", nombre)
    if os.path.exists(ruta_actual):
        return ruta_actual
    
    return buscar_ruta_recursiva(intentos[1:], nombre)

def cargar_img(nombre):
    posibles_directorios = [
        os.path.dirname(__file__),
        os.path.join(os.path.dirname(__file__), "..")
    ]
    
    ruta_final = buscar_ruta_recursiva(posibles_directorios, nombre)
    
    if ruta_final:
        try:
            return tk.PhotoImage(file=ruta_final)
        except Exception as e:
            print(f"⚠️ Error cargando imagen {nombre}: {e}")
            return None
    return None