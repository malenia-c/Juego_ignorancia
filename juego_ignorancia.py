## se importan las librerias necesarias
import random

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from conecta_bd import *
from ed_categoria import *
from ed_pregunta import *

## define la pantalla
pantalla = Tk()
pantalla.resizable(1,1)
pantalla.geometry("1200x900")

pantalla.title("Ignorancia-BD")


# =========================
# IMAGEN para el marcador, categoria, pregunta, SIGUIENTE
# =========================
img_marcador = PhotoImage(file=r"./im/fondo_marcador.png")
img_categoria = PhotoImage(file=r"./im/fondo_cate.png")
img_pregunta = PhotoImage(file=r"./im/fondo_preg.png")
img_siguiente = PhotoImage(file=r"./im/fondo_sig.png")
img_jug = PhotoImage(file=r"./im/fondo_jug.png")

# =========================
# IMAGEN PARA LOS BOTONES
# =========================
img_boton = PhotoImage(file=r"./im/fondo_boton.png")

img_label_jugador = PhotoImage(file=r"./im/fondo_label.png")

# =========================
# FONDO GENERAL DE LA VENTANA
# =========================
fondo_principal = PhotoImage(file=r"./im/CIE.png")

# Crear un Label con la imagen y expandirlo por toda la ventana
label_fondo = Label(pantalla, image=fondo_principal)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

label_fondo.lower()

# =========================
# VARIABLES
# =========================

seleccion = ()

str_preg = StringVar()
str_res1 = StringVar()
str_res2 = StringVar()
str_res3 = StringVar()
str_res4 = StringVar()
str_sig = StringVar()

correcto = 0

x1 = 10
x2 = 10
x3 = 10
x4 = 10

turno = 1
juego_terminado = False

WIN_ADVANCES = 11

adv1 = 0
adv2 = 0
adv3 = 0
adv_ignorancia = 0

# =========================
# NOMBRES Y MARCADOR
# =========================

nombre1 = StringVar()
nombre2 = StringVar()
nombre3 = StringVar()

victorias1 = 0
victorias2 = 0
victorias3 = 0

str_marcador = StringVar()

# =========================
# CANVAS
# =========================

canvas = Canvas( pantalla, width=1200, height=495, bg="lightblue2",
 highlightthickness=0
)

canvas.place(x=0, y=190)

# =========================
# FONDO
# =========================

fon = PhotoImage(file=r"./im/PISTA.png")

canvas.create_image(0,0,image=fon,
anchor=NW
)

# =========================
# FUNCIONES
# =========================

def validar_nombres(*args):
    """Bloquea el juego hasta que los 3 jugadores tengan un nombre escrito."""
    n1 = nombre1.get().strip()
    n2 = nombre2.get().strip()
    n3 = nombre3.get().strip()

    if n1 != "" and n2 != "" and n3 != "":
        categorias.config(state="readonly")
        sig.config(state=NORMAL)
    else:
        categorias.config(state=DISABLED)
        sig.config(state=DISABLED)

def mostrar_correcta():
    """Muestra un cuadro de texto con la respuesta correcta si fallan."""
    try:
        correcta = (
            str_res1.get() if correcto == 1 else
            str_res2.get() if correcto == 2 else
            str_res3.get() if correcto == 3 else
            str_res4.get()
        )
    except:
        correcta = "(desconocida)"

    messagebox.showinfo(
        "Respuesta incorrecta",
        f"La respuesta correcta es:\n{correcta}"
    )

def cargar_frames(ruta):
    """Carga todos los fotogramas de un archivo GIF."""
    frames = []
    i = 0
    while True:
        try:
            frames.append(PhotoImage(file=ruta, format=f'gif -index {i}'))
            i += 1
        except TclError:
            break
    return frames

def animar_gif(item_canvas, frames, indice=0):
    """Actualiza la imagen en el canvas para crear la animación."""
    canvas.itemconfig(item_canvas, image=frames[indice])
    
    siguiente_indice = (indice + 1) % len(frames)
    
    pantalla.after(100, animar_gif, item_canvas, frames, siguiente_indice)

def actualizar_marcador():

    n1 = nombre1.get()
    n2 = nombre2.get()
    n3 = nombre3.get()

    if n1 == "":
        n1 = "Jugador 1"

    if n2 == "":
        n2 = "Jugador 2"

    if n3 == "":
        n3 = "Jugador 3"

    marcador = (
        f"{n1}: {victorias1} victorias   |   "
        f"{n2}: {victorias2} victorias   |   "
        f"{n3}: {victorias3} victorias"
    )

    str_marcador.set(marcador)

def reiniciar_juego():

    global x1, x2, x3, x4
    global adv1, adv2, adv3, adv_ignorancia
    global turno, juego_terminado, seleccion

    x1 = 10
    x2 = 10
    x3 = 10
    x4 = 10

    adv1 = 0
    adv2 = 0
    adv3 = 0
    adv_ignorancia = 0

    turno = 1
    juego_terminado = False
    seleccion = ()

    canvas.coords(j1, x1, 40)
    canvas.coords(j2, x2, 160)
    canvas.coords(j3, x3, 260)
    canvas.coords(bu, x4, 390)

    str_sig.set("Jugador 1")

    str_preg.set("")
    str_res1.set("")
    str_res2.set("")
    str_res3.set("")
    str_res4.set("")

    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)

    entry_nombre1.config(state=NORMAL)
    entry_nombre2.config(state=NORMAL)
    entry_nombre3.config(state=NORMAL)
    
    categorias.config(state=DISABLED) 
    categorias.set('') 
    validar_nombres()

def fin_juego(mensaje):

    global juego_terminado
    global victorias1, victorias2, victorias3

    juego_terminado = True

    if nombre1.get() in mensaje:
        victorias1 += 1

    elif nombre2.get() in mensaje:
        victorias2 += 1

    elif nombre3.get() in mensaje:
        victorias3 += 1

    actualizar_marcador()

    repetir = messagebox.askyesno(
        "Fin del juego",
        mensaje + "\n\n¿Deseas jugar otra vez?"
    )

    if repetir:
        reiniciar_juego()

def avanza_jug():

    global x1, x2, x3
    global adv1, adv2, adv3

    if juego_terminado:
        return

    if turno == 1:

        x1 += 100
        adv1 += 1

        canvas.coords(j1, x1, 40)

        if adv1 >= WIN_ADVANCES:

            nombre = nombre1.get()

            if nombre == "":
                nombre = "Jugador 1"

            fin_juego(f"¡{nombre} ganó!")

    elif turno == 2:

        x2 += 100
        adv2 += 1

        canvas.coords(j2, x2, 160)

        if adv2 >= WIN_ADVANCES:

            nombre = nombre2.get()

            if nombre == "":
                nombre = "Jugador 2"

            fin_juego(f"¡{nombre} ganó!")

    elif turno == 3:

        x3 += 100
        adv3 += 1

        canvas.coords(j3, x3, 260)

        if adv3 >= WIN_ADVANCES:

            nombre = nombre3.get()

            if nombre == "":
                nombre = "Jugador 3"

            fin_juego(f"¡{nombre} ganó!")

def mover_ignorancia():

    global x4, adv_ignorancia

    x4 += 100
    adv_ignorancia += 1

    canvas.coords(bu, x4, 390)

    if adv_ignorancia >= WIN_ADVANCES and not juego_terminado:
        fin_juego("¡El slime ignorante ganó! Todos pierden.")

def desactivar_botones():

    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)

def opc1():

    desactivar_botones()

    if correcto == 1:
        avanza_jug()
    else:
        mostrar_correcta()
        mover_ignorancia()

def opc2():

    desactivar_botones()

    if correcto == 2:
        avanza_jug()
    else:
        mostrar_correcta()
        mover_ignorancia()

def opc3():

    desactivar_botones()

    if correcto == 3:
        avanza_jug()
    else:
        mostrar_correcta()
        mover_ignorancia()

def opc4():

    desactivar_botones()

    if correcto == 4:
        avanza_jug()
    else:
        mostrar_correcta()
        mover_ignorancia()

def sel_preg():

    global str_preg, correcto

    tam = len(seleccion)

    if tam != 0:

        n = random.randint(0, tam - 1)

        str_preg.set(seleccion[n][1])

        str_res1.set(seleccion[n][2])
        str_res2.set(seleccion[n][3])
        str_res3.set(seleccion[n][4])
        str_res4.set(seleccion[n][5])

        try:
            correcto = int(seleccion[n][6])
        except:
            correcto = seleccion[n][6]

        if not juego_terminado:

            r1.config(state=NORMAL)
            r2.config(state=NORMAL)
            r3.config(state=NORMAL)
            r4.config(state=NORMAL)

def pregunta(event):

    global seleccion

    cat = event.widget.get()

    seleccion = recupera_preguntas(cat)

    sel_preg()
    # 
    categorias.config(state=DISABLED)

def pregunta_sig():

    global seleccion, turno

    if juego_terminado:
        return

    entry_nombre1.config(state=DISABLED)
    entry_nombre2.config(state=DISABLED)
    entry_nombre3.config(state=DISABLED)

    cat = categorias.get()

    seleccion = recupera_preguntas(cat)

    sel_preg()

    turno += 1

    if turno > 3:
        turno = 1

    if turno == 1:

        nombre_turno = nombre1.get()

        if nombre_turno == "":
            nombre_turno = "Jugador 1"

    elif turno == 2:

        nombre_turno = nombre2.get()

        if nombre_turno == "":
            nombre_turno = "Jugador 2"

    else:

        nombre_turno = nombre3.get()

        if nombre_turno == "":
            nombre_turno = "Jugador 3"

    str_sig.set(nombre_turno)

# =========================
# CATEGORIAS
# =========================

L_cats = recupera_categoria()
style = ttk.Style()
style.configure("Custom.TCombobox", font=("Arial Black", 18, "bold"))
pantalla.option_add('*TCombobox*Listbox.font', ("Arial Black", 18, "bold"))

categorias = ttk.Combobox(pantalla, font=("Arial Black", 18, "bold"),state=DISABLED)
categorias['values'] = L_cats
categorias.place(x=170, y=10)
categorias.bind("<<ComboboxSelected>>", pregunta)
# Mostrar categoria seleccionada (recuadro)
eti_cat = Label(pantalla, image=img_categoria,compound=CENTER, fg="Pink4", text="Categoria", font=("Arial Black", 18, "bold"),
bg="purple4", activebackground="purple4", bd=0, highlightthickness=0, relief=FLAT, padx=0, pady=0, cursor="hand2")
eti_cat.place(x=10, y=10)


# =========================
# BOTON SIGUIENTE
# =========================

sig = Button(pantalla, text="Siguiente", command=pregunta_sig, font=("Arial Black", 12, "bold"),bg="purple4", 
 activebackground="purple4", bd=0, highlightthickness=0, relief=FLAT,padx=0, pady=0, cursor="hand2",
 image=img_siguiente,compound=CENTER, fg="Pink4", state=DISABLED
)


sig.place(x=650, y=18)

# =========================
# TURNO
# =========================

str_sig.set("Jugador 1")

sig_jug = Label(pantalla,compound=CENTER, fg="Pink4", image=img_jug, textvariable=str_sig,
 font=("Arial Black", 16, "bold"),bg="purple4", 
 activebackground="purple4", bd=0, highlightthickness=0, relief=FLAT,padx=0, pady=0, cursor="hand2"
)

sig_jug.place(x=850, y=20)

# =========================
# PREGUNTA
# =========================

eti = Label(pantalla, image=img_pregunta,compound=CENTER, fg="Pink4", text="Pregunta",
 font=("Arial Black", 16, "bold"),bg="purple4", activebackground="purple4", bd=0, highlightthickness=0, relief=FLAT,
 padx=0, pady=0, cursor="hand2"
)

eti.place(x=10, y=70)

pre = Entry(pantalla, textvariable=str_preg, font=("Arial Black", 16, "bold"), bg="white",
 width=70, state="readonly"  # Bloquea la escritura manual
)

pre.place(x=170, y=70)

# =========================
# RESPUESTAS
# =========================

r1 = Button(pantalla, textvariable=str_res1, command=opc1, image=img_boton, compound=CENTER,
            font=("Arial Black", 12, "bold"), fg="white", bg="purple4", activebackground="purple4", 
            bd=0, highlightthickness=0, relief=FLAT, padx=0, pady=0, cursor="hand2")
r1.place(x=70, y=130)

r2 = Button(pantalla, textvariable=str_res2, command=opc2, image=img_boton, compound=CENTER,
            font=("Arial Black", 12, "bold"), fg="white", bg="purple4", activebackground="purple4", 
            bd=0, highlightthickness=0, relief=FLAT, padx=0, pady=0, cursor="hand2")
r2.place(x=340, y=130)

r3 = Button(pantalla, textvariable=str_res3, command=opc3, image=img_boton, compound=CENTER,
            font=("Arial Black", 12, "bold"), fg="white", bg="purple4", activebackground="purple4", 
            bd=0, highlightthickness=0, relief=FLAT, padx=0, pady=0, cursor="hand2")
r3.place(x=610, y=130)

r4 = Button(pantalla, textvariable=str_res4, command=opc4, image=img_boton, compound=CENTER,
            font=("Arial Black", 12, "bold"), fg="white", bg="purple4", activebackground="purple4", 
            bd=0, highlightthickness=0, relief=FLAT, padx=0, pady=0, cursor="hand2")
r4.place(x=880, y=130)

# =========================
# IMAGENES GIF ANIMADAS
# =========================

frames_ju1 = cargar_frames(r"./im/slime1.gif")
frames_ju2 = cargar_frames(r"./im/slime2.gif")
frames_ju3 = cargar_frames(r"./im/slime3.gif")
frames_bur = cargar_frames(r"./im/slime4.gif")

j1 = canvas.create_image(10, 40, image=frames_ju1[0], anchor=NW)
j2 = canvas.create_image(10, 160, image=frames_ju2[0], anchor=NW)
j3 = canvas.create_image(10, 260, image=frames_ju3[0], anchor=NW)
bu = canvas.create_image(10, 390, image=frames_bur[0], anchor=NW)

animar_gif(j1, frames_ju1)
animar_gif(j2, frames_ju2)
animar_gif(j3, frames_ju3)
animar_gif(bu, frames_bur)


# =========================
# MARCADOR 
# =========================

actualizar_marcador()

Label(pantalla,  textvariable=str_marcador, image=img_marcador,compound=CENTER, fg="black", font=("Arial Black", 11, "bold"), 
 bg="purple4", activebackground="purple4", bd=0, highlightthickness=0, relief=FLAT, padx=0, pady=0, cursor="hand2", 
 width=786
).place(x=10, y=700)

# =========================
# NOMBRES 
# =========================

Label(pantalla, text="Jugador 1", image=img_label_jugador, compound=CENTER, fg="black", font=("Arial Black", 12, "bold"), bd=0, highlightthickness=0).place(x=20, y=740)
entry_nombre1 = Entry(pantalla, textvariable=nombre1, font=("Arial Black", 12), width=18)
entry_nombre1.place(x=20, y=770)

Label(pantalla, text="Jugador 2", image=img_label_jugador, compound=CENTER, fg="black", font=("Arial Black", 12, "bold"), bd=0, highlightthickness=0).place(x=320, y=740)
entry_nombre2 = Entry(pantalla, textvariable=nombre2, font=("Arial Black", 12), width=18)
entry_nombre2.place(x=320, y=770)

Label(pantalla, text="Jugador 3", image=img_label_jugador, compound=CENTER, fg="black", font=("Arial Black", 12, "bold"), bd=0, highlightthickness=0).place(x=620, y=740)
entry_nombre3 = Entry(pantalla, textvariable=nombre3, font=("Arial Black", 12), width=18)
entry_nombre3.place(x=620, y=770)

# =========================
# RASTREADORES AUTOMÁTICOS
# =========================
nombre1.trace_add("write", validar_nombres)
nombre2.trace_add("write", validar_nombres)
nombre3.trace_add("write", validar_nombres)

validar_nombres()

pantalla.mainloop() 

