# ==========================================
# INTERFAZ: PANTALLA DE PELEA
# ==========================================
import tkinter as tk
import sys
import os
from Interfaz.componentes import cargar_img
from Logic.combate import inicializar_batalla, procesar_ataque_recursivo, gestionar_captura
from Logic.datos import db_personajes 
from Logic.audio import reproducir_musica, detener_musica

# ==========================================
# UTILIDADES Y MANEJO DE ESTADO
# ==========================================
def limpiar_recursivo(widgets):
    if not widgets: return
    widgets[0].destroy()
    limpiar_recursivo(widgets[1:])

def extraer_nombres_recursivo(lista):
    if not lista: return []
    return [lista[0]["nombre"]] + extraer_nombres_recursivo(lista[1:])

def reiniciar_juego():
    detener_musica()
    python = sys.executable
    os.execl(python, python, *sys.argv)

def crear_pantalla_pelea(frame_padre, estado_juego, callback_regreso, callback_victoria):
    limpiar_recursivo(frame_padre.winfo_children())
    reproducir_musica("pelea.wav")
    datos = inicializar_batalla(estado_juego["personajes_elegidos"])
    
    canvas = tk.Canvas(frame_padre, width=1280, height=720, bg="#1a1a1a", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.refs = {}

    def obtener_nombre_seguro(pj):
        if not pj: return "Desconocido"
        return pj.get("nombre") or pj.get("name") or pj.get("Nombre") or "Desconocido"

# ==========================================
# RENDERIZADO VISUAL Y EFECTOS
# ==========================================
    def mostrar_game_over():
        reproducir_musica("menu.wav")
        canvas.create_rectangle(0, 0, 1280, 720, fill="black", stipple="gray50", tags="dinamico")
        canvas.create_text(640, 300, text="DERROTA TOTAL", font=("Consolas", 80, "bold"), fill="#c0392b", tags="dinamico")
        canvas.create_text(640, 400, text="Te has quedado sin personajes. Los Hollows han ganado.", 
                          font=("Consolas", 20), fill="white", tags="dinamico")
        btn_retry = tk.Button(frame_padre, text="REINTENTAR DESDE EL INICIO", font=("Consolas", 14, "bold"),
                             bg="#2ecc71", fg="white", padx=20, pady=10, command=reiniciar_juego)
        canvas.create_window(640, 500, window=btn_retry, tags="dinamico")

    def mostrar_efecto_critico(lado_defensor):
        x_pos = 350 if lado_defensor == "jugador" else 930
        y_pos = 280
        canvas.create_text(x_pos+3, y_pos+3, text="¡GOLPE CRÍTICO!", 
                           font=("Consolas", 28, "bold", "italic"), fill="black", tags="efecto_critico")
        canvas.create_text(x_pos, y_pos, text="¡GOLPE CRÍTICO!", 
                           font=("Consolas", 28, "bold", "italic"), fill="#f1c40f", tags="efecto_critico")
        
        canvas.tag_raise("efecto_critico")
        
        def safe_delete():
            if canvas.winfo_exists():
                canvas.delete("efecto_critico")
                
        frame_padre.after(1000, safe_delete)

    def actualizar_escena_recursiva(lista_bandos):
        if len(lista_bandos) == 2:
            canvas.delete("dinamico")
            progreso = estado_juego.get("progreso", 0)
            bg = cargar_img(f"fondo_pelea_{progreso}.png") or cargar_img("fondo_pelea.png")
            if bg:
                canvas.refs["bg"] = bg
                canvas.create_image(0, 0, image=bg, anchor="nw")

        if not lista_bandos: return

        lado, p = lista_bandos[0]
        if p:
            nombre = obtener_nombre_seguro(p)
            x_pos = 100 if lado == "jugador" else 780
            info_db = db_personajes.get(nombre, {})
            hp_max = info_db.get("hp", 100)
            hp_actual = p.get("hp", 0)
            ratio = (hp_actual / hp_max) if hp_max > 0 else 0
            
            canvas.create_rectangle(x_pos, 60, x_pos+400, 85, fill="#c0392b", outline="white", tags="dinamico")
            canvas.create_rectangle(x_pos, 60, x_pos+(400*ratio), 85, fill="#2ecc71", outline="white", tags="dinamico")
            canvas.create_text(x_pos+200, 45, text=f"{nombre}: {hp_actual} HP", 
                               fill="white", font=("Consolas", 12, "bold"), tags="dinamico")

            sprite_img = cargar_img(p.get("sprite"))
            if sprite_img:
                canvas.refs[f"spr_{lado}"] = sprite_img
                px = 350 if lado == "jugador" else 930
                canvas.create_image(px, 450, image=sprite_img, tags="dinamico")

        actualizar_escena_recursiva(lista_bandos[1:])

# ==========================================
# LÓGICA DE TURNOS Y COMBATE
# ==========================================
    def manejar_ataque():
        btn_atk.config(state="disabled")
        btn_sw.config(state="disabled")
        ko_hollow, danio_real, es_critico = procesar_ataque_recursivo(datos, True)
        
        actualizar_escena_recursiva([("jugador", datos.get("activo_jugador")), ("hollow", datos.get("activo_hollow"))])
        
        if es_critico:
            mostrar_efecto_critico("hollow")
            
        if ko_hollow:
            gestionar_captura(datos, False) 
            if not datos.get("equipo_hollow"): 
                estado_juego["progreso"] = estado_juego.get("progreso", 0) + 1
                estado_juego["personajes_elegidos"] = extraer_nombres_recursivo(datos["equipo_jugador"])
                estado_juego["score"] = estado_juego.get("score", 0) + datos.get("puntos_jugador", 0)
                reproducir_musica("menu.wav")
                return callback_regreso() 
            
            datos["activo_hollow"] = datos["equipo_hollow"][0]
            actualizar_escena_recursiva([("jugador", datos.get("activo_jugador")), ("hollow", datos.get("activo_hollow"))])
            btn_atk.config(state="normal")
            btn_sw.config(state="normal")
        else:
            frame_padre.after(1000, turno_enemigo)

    def turno_enemigo():
        if not datos["activo_jugador"]: return 
        ko_jugador, danio_real, es_critico = procesar_ataque_recursivo(datos, False)
        
        actualizar_escena_recursiva([("jugador", datos.get("activo_jugador")), ("hollow", datos.get("activo_hollow"))])
        
        if es_critico:
            mostrar_efecto_critico("jugador")
            
        if ko_jugador:
            gestionar_captura(datos, True) 
            if not datos.get("equipo_jugador"):
                return mostrar_game_over()
            datos["activo_jugador"] = None
            abrir_mini_menu_seleccion(es_turno_consumido=False)
        else:
            btn_atk.config(state="normal")
            btn_sw.config(state="normal")

# ==========================================
# MENÚ DE CAMBIO DE PERSONAJE
# ==========================================
    def abrir_mini_menu_seleccion(es_turno_consumido=False):
        btn_atk.config(state="disabled")
        btn_sw.config(state="disabled")
        
        ventana_sel = tk.Toplevel(frame_padre)
        ventana_sel.title("Selección")
        ventana_sel.geometry("800x350")
        ventana_sel.configure(bg="#0a0a0a")
        ventana_sel.transient(frame_padre)
        ventana_sel.grab_set() 
        
        def no_cerrar(): pass
        if not datos["activo_jugador"]: ventana_sel.protocol("WM_DELETE_WINDOW", no_cerrar)
        
        tk.Label(ventana_sel, text="¿A QUIÉN ENVIARÁS AL CAMPO?", font=("Consolas", 16, "bold"), 
                 bg="#0a0a0a", fg="#f1c40f").pack(pady=10)
        
        frame_scroll = tk.Frame(ventana_sel, bg="#0a0a0a")
        frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas_sel = tk.Canvas(frame_scroll, bg="#0a0a0a", highlightthickness=0, height=230)
        scroll_x = tk.Scrollbar(frame_scroll, orient="horizontal", command=canvas_sel.xview)
        canvas_sel.configure(xscrollcommand=scroll_x.set)
        scroll_x.pack(side="bottom", fill="x")
        canvas_sel.pack(side="top", fill="both", expand=True)
        
        frame_opciones = tk.Frame(canvas_sel, bg="#0a0a0a")
        canvas_sel.create_window((0, 0), window=frame_opciones, anchor="nw")
        frame_opciones.bind("<Configure>", lambda e: canvas_sel.configure(scrollregion=canvas_sel.bbox("all")))
        
        generar_botones_recursivo(frame_opciones, datos.get("equipo_jugador", []), ventana_sel, True, es_turno_consumido)

    def generar_botones_recursivo(contenedor, lista_pjs, ventana_ref, es_inicio, es_turno_consumido):
        if not lista_pjs: return
        pj = lista_pjs[0]
        nombre_pj = obtener_nombre_seguro(pj)
        vida_actual = pj.get("hp", 0)
        info_db = db_personajes.get(nombre_pj, {})
        img_btn = cargar_img(str(pj.get("img") or info_db.get("img") or "default.png"))
        
        btn = tk.Button(contenedor, text=f"{nombre_pj.upper()}\nHP: {vida_actual}",
                        image=img_btn, compound="top", width=160, height=200,
                        font=("Consolas", 10, "bold"), bg="#2c3e50",
                        fg="white", command=lambda p=pj: confirmar_seleccion(p, ventana_ref, es_turno_consumido))
        btn.pack(side="left", padx=15, pady=10)
        btn.image = img_btn 
        generar_botones_recursivo(contenedor, lista_pjs[1:], ventana_ref, es_inicio, es_turno_consumido)

    def confirmar_seleccion(pj_elegido, ventana, es_turno_consumido):
        if datos["activo_jugador"] == pj_elegido and es_turno_consumido:
            ventana.destroy()
            btn_atk.config(state="normal")
            btn_sw.config(state="normal")
            return

        datos["activo_jugador"] = pj_elegido
        ventana.destroy()
        actualizar_escena_recursiva([("jugador", datos.get("activo_jugador")), ("hollow", datos.get("activo_hollow"))])
        
        if es_turno_consumido:
            frame_padre.after(1000, turno_enemigo)
        else:
            btn_atk.config(state="normal")
            btn_sw.config(state="normal")

# ==========================================
# INICIALIZACIÓN DE BOTONES
# ==========================================
    btn_atk = tk.Button(frame_padre, text="ATAQUE", font=("Consolas", 14, "bold"), 
                        bg="#e74c3c", fg="white", width=12, command=manejar_ataque)
    btn_sw = tk.Button(frame_padre, text="CAMBIAR", font=("Consolas", 14, "bold"), 
                       bg="#3498db", fg="white", width=12, command=lambda: abrir_mini_menu_seleccion(es_turno_consumido=True))
    
    canvas.create_window(540, 650, window=btn_atk)
    canvas.create_window(740, 650, window=btn_sw)
    
    btn_atk.config(state="disabled")
    btn_sw.config(state="disabled")
    abrir_mini_menu_seleccion(es_turno_consumido=False)