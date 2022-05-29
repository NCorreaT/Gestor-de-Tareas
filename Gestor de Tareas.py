from tkinter import *
from tkinter import messagebox
import sqlite3

conexion = sqlite3.connect("Tarea.db")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE if not exists nota (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        descripcion TEXT NOT NULL,
        completado BOOLEAN NOT NULL
    );
""")

conexion.commit()

root = Tk()
root.title("Gestor de Tareas")

ancho = 600
largo = 600
pantalla_ancho = root.winfo_screenwidth()
pantalla_largo = root.winfo_screenheight()
x = (pantalla_ancho / 2) - (ancho / 2)#Para centrar la ventana en la pantalla
y = (pantalla_largo / 4) - (largo / 4)
root.geometry("%dx%d+%d+%d" % (ancho, largo, x, y))
root.iconbitmap("C:/Users/niko_/Desktop/Python/Gestor de Tareas/cuaderno.ico")


def nueva():#Crear nueva tarea
    todo = caja_texto.get()
    if todo:
        cursor.execute("""
            INSERT INTO nota (descripcion,completado) values (?, ?)
        """, (todo, False))
        
        conexion.commit()
        caja_texto.delete(0, END)
        cargar_datos()
    else:
        messagebox.showerror("Error","Debe ingresar una tarea")


def cargar_datos():#Listar las tareas
    rows = cursor.execute("SELECT id, datetime(creado_en ,'localtime') as creado_en, descripcion,completado FROM nota").fetchall()
 
    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):#Mostrar las tareas en la grilla
        id = rows[i][0]
        completado = rows[i][3]
        descripcion = rows[i][2]
        fecha = rows[i][1]
        
        color = "black" if completado else "#666666"
          
        check = Checkbutton(frame, text=descripcion, fg=color, width=40, anchor="w", command=estado(id))
        check.grid(row=i, column=0,pady=10, sticky="w")
        
        lb_fecha = Label(frame, text=fecha, fg=color)
        lb_fecha.grid(row=i, column=1, padx=20, ipadx=10)

        btn_eliminar = Button(frame, text="Eliminar", font=("Arial",9,"bold"), command=eliminar(id))
        btn_eliminar.grid(row=i, column=2, ipadx=20, ipady=5)

        check.select() if completado else check.deselect()
    
    
def estado(id):#Buscar el estado de la tarea
    def _estado():
        todo = conexion.execute("SELECT * FROM nota WHERE id = ?", (id, )).fetchone()
        cursor.execute("UPDATE nota SET completado = ? WHERE id = ?", (not todo[3], id))
        conexion.commit()
        cargar_datos()

    return _estado


def eliminar(id):#Eliminar la tarea seleccionada
    def _eliminar():
        respuesta = messagebox.askokcancel("Seguro?", f"Estas seguro de querer eliminar esta tarea?")
        if respuesta:
            cursor.execute("DELETE FROM nota WHERE id = ?", (id, ))
            conexion.commit()
            cargar_datos()
        else:
            pass

    return _eliminar


lb_tarea = Label(root, text="Tarea", font=("Arial",15, "bold"), padx=10, pady=20)
lb_tarea.grid(row=1, column=0)

caja_texto = Entry(root, width=60)
caja_texto.grid(row=1, column=1,ipady=5, ipadx=5)

btn_nuevo = Button(root, text="Nuevo", font=("Arial",10,"bold"), bg="#ddd", command=nueva)
btn_nuevo.grid(row=1, column=2, ipadx=20, ipady=5 , padx="10")

frame = LabelFrame(root, text="Mis tareas", font=("Arial",11,"bold"), padx=5, pady=5)
frame.grid(row=2, column=0, columnspan=3, sticky='nswe', padx=5)

cargar_datos()

caja_texto.focus()
root.bind("<Return>", lambda x : nueva())#Agregar nueva tarea con enter 

root.mainloop()

