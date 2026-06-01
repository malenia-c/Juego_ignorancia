from tkinter import*
from tkinter import ttk
from conecta_bd import*
from ed_pregunta import*

def manipula_categorias():
    pantalla_cat = Toplevel()
    pantalla_cat.resizable(1, 1)
    pantalla_cat.geometry("750x350")
    pantalla_cat.config(background="Light Sky Blue")
    pantalla_cat.title("Catalogo de Categorias")
    str_cat = StringVar()

    marco_per = Frame(pantalla_cat)
    marco_per.pack()
    marco_per.place(x=20, y=100)
    ver_sb = ttk.Scrollbar(marco_per, orient="vertical")
    ver_sb.pack(side=RIGHT, fill='y')

    Tabl_cat = ttk.Treeview(marco_per, columns=("col1"), yscrollcommand=ver_sb.set)
    Tabl_cat.column("#0", width=155)
    Tabl_cat.column("col1", width=500)
    Tabl_cat.heading("#0", text="Id Categoria")
    Tabl_cat.heading("col1", text="Descripcion")
    Tabl_cat.pack()

    ver_sb.config(command=Tabl_cat.yview)

    def recupera_db():
        for record in Tabl_cat.get_children():
            Tabl_cat.delete(record)
    
        categs = tabla_categorias()
        for categ in categs:
            Tabl_cat.insert(parent="", index="end", iid=categ[0], text=str(categ[0]),alues=(str(categ[1]).replace(' ', '_')))

    def agrega_cat():
        insertar_categoria(str_cat.get())
        recupera_db

    def borra_catsel():
        ab = Tabl_cat.selection()[0]
        borra_categoria(ab)
        recupera_db()

    def selec_cat():
        ab = Tabl_cat.selection()[0]
        datos = selec_categoria(ab)
        str_cat.set(datos[1])

    def modif_catsel():
        ab = Tabl_cat.selection()[0]
        modif_categoria(ab, str_cat.get())
        recupera_db()

    recupera_db()
    et=Label(pantalla_cat,text="categoria", bg="ligh sky blue", font="Helvetica 14 bold")
    et.place(x=120,Y=20)

    def edita_pretguntas():
        global datos 
        print(datos)


    str_cat.set("")
    pre = Entry(pantalla_cat, textvariable=str_cat, font="Helvetica 14 bold", bg="Lavender", whidt=50)
    pre.place(x=120, y=20)
    b_per = Button(pantalla_cat, text="Agregar categorías",command=agrega_cat,fg="white",bg="red4",font="Helvetica 12 bold").place(x=570,y=20)
    b_modif_cat=Button(pantalla_cat,text="Modifica categoría",command=modif_catsel,fg="white",bg="red4",font="Helvetica 12 bold",width=15).place(x=10,y=10)
    b_borra_cat=Button(pantalla_cat,text="Borrar categorías",command=borra_catsel,fg="white",bg="red4",font="Helvetica 12 bold",width=15).place(x=450,y=250)
    b_selec_cat=Button(pantalla_cat,text="Selecciona Categoría",command=selec_cat,fg="white",bg="red4",font="Helvetica 12 bold",width=20).place(x=250,y=300)

    pantalla_cat.mainloop()




