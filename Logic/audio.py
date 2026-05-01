# ==========================================
# LOGIC: MOTOR DE AUDIO
# ==========================================
import subprocess
import os

reproductor_actual = None
tema_actual = None

# ==========================================
# CONTROL DE REPRODUCCIÓN
# ==========================================
def reproducir_musica(nombre_archivo):
    global reproductor_actual, tema_actual
    
    if tema_actual == nombre_archivo and reproductor_actual is not None:
        if reproductor_actual.poll() is None: 
            return
            
    detener_musica()
    
    ruta_este_archivo = os.path.abspath(__file__)
    directorio_raiz = os.path.dirname(os.path.dirname(ruta_este_archivo))
    ruta = os.path.join(directorio_raiz, "Interfaz", "Assets", nombre_archivo)
    
    if os.path.exists(ruta):
        reproductor_actual = subprocess.Popen(
            ['aplay', '-q', ruta], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        tema_actual = nombre_archivo
    else:
        print(f"⚠️ Audio no encontrado en: {ruta}")

# ==========================================
# GESTIÓN DE PROCESOS
# ==========================================
def detener_musica():
    global reproductor_actual, tema_actual
    if reproductor_actual:
        reproductor_actual.terminate()
        reproductor_actual.wait() 
        reproductor_actual = None
        tema_actual = None