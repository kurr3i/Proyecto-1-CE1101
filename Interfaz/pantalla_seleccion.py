import tkinter as tk
import os
from tkinter import messagebox
from Logic.datos import db_personajes
from Logic.motor import obtener_stats, estado_juego
from Interfaz.componentes import cargar_img

boton_parpadeando = None
personaje_a_cambiar = None
fase_intercambio = False
seleccionados_actualmente = []
botones_pj = {}
lbl_stats_dinamicos = None
btn_guardar_pj = None

def limpiar_widgets_recursivo(widgets):
    if not widgets:
        return
    widgets[0].destroy()
    limpiar_widgets_recursivo(widgets[1:])

def verificar_estado_seleccion():
    if len(seleccionados_actualmente) == 3:
        btn_guardar_pj.config(state="normal", bg="#2ecc71", fg="white")
    else:
        btn_guardar_pj.config(state="disabled", bg="gray", fg="black")

def parpadear_amarillo(boton, ventana_ref):
    if fase_intercambio and boton_parpadeando == boton:
        color_actual = boton.cget("bg")
        nuevo_color = "#f1c40f" if color_actual != "#f1c40f" else "#e67e22"
        boton.config(bg=nuevo_color)
        ventana_ref.after(400, lambda: parpadear_amarillo(boton, ventana_ref))
    else:
        restablecer_colores_recursivo(list(botones_pj.items()))

def restablecer_colores_recursivo(items):
    if not items:
        return
    nombre, btn_ref = items[0]
    btn_ref.config(bg="#2ecc71" if nombre in seleccionados_actualmente else "#f0f0f0")
    restablecer_colores_recursivo(items[1:])

def seleccionar_personaje_grid(nombre, ventana_ref):
    global seleccionados_actualmente, personaje_a_cambiar, fase_intercambio, boton_parpadeando
    boton = botones_pj[nombre]

    if nombre in seleccionados_actualmente:
        if personaje_a_cambiar == nombre:
            personaje_a_cambiar = None
            fase_intercambio = False
            boton_parpadeando = None
            boton.config(bg="#2ecc71")
        else:
            restablecer_colores_recursivo(list(botones_pj.items()))
            personaje_a_cambiar = nombre
            fase_intercambio = True
            boton_parpadeando = boton
            parpadear_amarillo(boton, ventana_ref)
        return

    if fase_intercambio:
        viejo_nombre = personaje_a_cambiar
        idx = seleccionados_actualmente.index(viejo_nombre)
        seleccionados_actualmente[idx] = nombre
        fase_intercambio = False
        personaje_a_cambiar = None
        boton_parpadeando = None
        botones_pj[viejo_nombre].config(bg="#f0f0f0", relief="raised")
        boton.config(bg="#2ecc71", relief="sunken")
        verificar_estado_seleccion()
        return

    if len(seleccionados_actualmente) < 3:
        seleccionados_actualmente.append(nombre)
        boton.config(bg="#2ecc71", relief="sunken")
    else:
        messagebox.showwarning("Equipo Lleno", "¡Solo puedes llevar 3! Haz clic en uno verde para cambiarlo.")
    verificar_estado_seleccion()

def mostrar_detalles(nombre):
    info = db_personajes[nombre]
    # Usamos .get() con valores por defecto para que no explote si la llave cambia
    rol = info.get('ROL') or info.get('rol') or "Desconocido"
    hp = info.get('hp') or info.get('VIDA') or 0
    atk = info.get('atk') or info.get('atq') or info.get('ATAQUE') or 0
    df = info.get('def') or info.get('DEFENSA') or 0

    texto = (f"NOMBRE: {nombre}\n\n"
             f"ROL: {rol}\n"
             f"❤️ HP: {hp}\n"
             f"⚔️ ATQ: {atk}\n"
             f"🛡️ DEF: {df}")
    lbl_stats_dinamicos.config(text=texto, fg="white")

def renderizar_grid_recursivo(contenedor, nombres, ventana_ref, fila, columna):
    if not nombres:
        return
    
    nombre = nombres[0]
    datos = db_personajes[nombre]
    
    cajita = tk.Frame(contenedor, width=130, height=160, bg="#1a1a1a")
    cajita.grid(row=fila, column=columna, padx=5, pady=5)
    cajita.pack_propagate(False)
    
    img_pj = cargar_img(datos["img"])
    if img_pj:
        cajita.img_ref = img_pj 
    
    btn = tk.Button(cajita, image=img_pj if img_pj else "", relief="raised", bg="#f0f0f0",
                    command=lambda n=nombre: seleccionar_personaje_grid(n, ventana_ref))
    btn.pack(fill="both", expand=True)
    botones_pj[nombre] = btn
    
    btn.bind("<Enter>", lambda e, n=nombre: mostrar_detalles(n))
    btn.bind("<Leave>", lambda e: lbl_stats_dinamicos.config(text="Pasa el mouse...", fg="gray"))
    
    tk.Label(cajita, text=nombre.split(" (")[0], font=("Consolas", 8), bg="#1a1a1a", fg="white").pack()
    
    if nombre in seleccionados_actualmente:
        btn.config(bg="#2ecc71", relief="sunken")
        
    nuevo_c = columna + 1
    nuevo_f = fila
    if nuevo_c > 4:
        nuevo_c = 0
        nuevo_f = fila + 1
        
    renderizar_grid_recursivo(contenedor, nombres[1:], ventana_ref, nuevo_f, nuevo_c)

def refrescar_pantalla_seleccion(frame_padre, callback_volver):
    global btn_guardar_pj, lbl_stats_dinamicos, botones_pj
    botones_pj = {} 
    ventana_ref = frame_padre.winfo_toplevel()
    limpiar_widgets_recursivo(frame_padre.winfo_children())
    
    canvas = tk.Canvas(frame_padre, width=1280, height=720, highlightthickness=0, bg="#0f0f0f")
    canvas.pack(fill="both", expand=True)
    
    img_fondo = cargar_img("fondo_personajes.png")
    if img_fondo:
        canvas.bg_ref = img_fondo 
        canvas.create_image(0, 0, image=img_fondo, anchor="nw")

    frame_info = tk.Frame(frame_padre, bg="#1a1a1a", bd=3, relief="ridge", width=250, height=400)
    canvas.create_window(1100, 360, window=frame_info)
    frame_info.pack_propagate(False)
    
    tk.Label(frame_info, text="STATS", font=("Consolas", 16, "bold"), bg="#1a1a1a", fg="#f1c40f").pack(pady=10)
    lbl_stats_dinamicos = tk.Label(frame_info, text="Pasa el mouse...", font=("Consolas", 12), 
                                   bg="#1a1a1a", fg="white", justify="left")
    lbl_stats_dinamicos.pack(pady=20, padx=10)
    
    contenedor_grid = tk.Frame(frame_padre, bg="#1a1a1a")
    canvas.create_window(540, 360, window=contenedor_grid)

    renderizar_grid_recursivo(contenedor_grid, list(db_personajes.keys()), ventana_ref, 0, 0)

    btn_guardar_pj = tk.Button(frame_padre, text="CONFIRMAR EQUIPO", state="disabled",
                               font=("Consolas", 14, "bold"), 
                               command=lambda: finalizar(callback_volver))
    canvas.create_window(640, 660, window=btn_guardar_pj)
    verificar_estado_seleccion()

def construir_equipo_recursivo(nombres):
    if not nombres:
        return []
    
    nombre = nombres[0]
    stats = db_personajes.get(nombre, {})
    
    pj = {
        "nombre": nombre,
        "hp": stats.get("hp", 100),
        "atq": stats.get("atq", 50),
        "def": stats.get("def", 50),
        "img": stats.get("img", ""),
        "sprite": stats.get("sprite", f"{nombre.lower()}_s.png")
    }
    
    return [pj] + construir_equipo_recursivo(nombres[1:])

def finalizar(callback):
    global fase_intercambio, personaje_a_cambiar
    fase_intercambio = False
    personaje_a_cambiar = None
    estado_juego["personajes_elegidos"] = construir_equipo_recursivo(seleccionados_actualmente)
    callback()