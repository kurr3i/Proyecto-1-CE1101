import subprocess
import os

reproductor_actual = None
tema_actual = None

def reproducir_musica(nombre_archivo):
    global reproductor_actual, tema_actual
    
    if tema_actual == nombre_archivo and reproductor_actual is not None:
        if reproductor_actual.poll() is None: 
            return
            
    detener_musica()
    
    # 1. Obtenemos la ruta absoluta de este mismo archivo (audio.py)
    ruta_este_archivo = os.path.abspath(__file__)
    
    # 2. Hacemos el "cd .." dos veces (salimos de audio.py, salimos de Logic)
    # Esto nos deja parados exactamente en la raíz del proyecto (Proyecto_Intro)
    directorio_raiz = os.path.dirname(os.path.dirname(ruta_este_archivo))
    
    # 3. Entramos a Interfaz/Assets
    ruta = os.path.join(directorio_raiz, "Interfaz", "Assets", nombre_archivo)
    
    if os.path.exists(ruta):
        reproductor_actual = subprocess.Popen(
            ['aplay', '-q', ruta], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        tema_actual = nombre_archivo
    else:
        # Ahora el error te imprimirá la ruta completa exacta que intentó buscar
        print(f"⚠️ Audio no encontrado en: {ruta}")

def detener_musica():
    global reproductor_actual, tema_actual
    if reproductor_actual:
        reproductor_actual.terminate()
        reproductor_actual.wait() 
        reproductor_actual = None
        tema_actual = None