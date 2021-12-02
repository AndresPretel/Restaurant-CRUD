from tkinter import StringVar,LabelFrame,Button,Label,Entry,Tk
from tkinter import ttk
from connexion import *
import pywhatkit


#Ventana Principal
ventana=Tk()
ventana.title("Software Administracion y Notificacion de Pedidos")
ventana.geometry("600x500")

db=DataBase()
##
modificar= False
turno=int()
nombre= StringVar()
apellido= StringVar()
telefono= StringVar()

#Funciones
def seleccionar(event):
    turno =tvPedidos.selection()[0]
    if int(id)>0:
        nombre.set(tvPedidos.item(nombre,"values")[2])
        apellido.set(tvPedidos.item(apellido,"values")[3])
        telefono.set(tvPedidos.item(telefono,"values")[4])

#Funcion Cambio Texto Boton
def modificarFalse():
    global modificar
    modificar=False
    tvPedidos.config(selectmode="none")
    btnNuevo.config(text="Guardar")
    btnModificar.config(text="Seleccionar")
    btnEliminar.config(state="disabled")

#Funcion cambia Texto Boton
def modificarTrue():
    global modificar
    modificar=True
    tvPedidos.config(selectmode="browse")
    btnNuevo.config(text="Nuevo")
    btnModificar.config(text="Modificar")
    btnEliminar.config(state="normal")
def validar():
    return len(nombre.get()) and len(apellido.get()) and len(telefono.get())

def limpiar():
    nombre.set("")
    apellido.set("")
    telefono.set("")

def vaciar_tabla():
    filas= tvPedidos.get_children()
    for fila in filas:
        tvPedidos.delete(fila)
        
def llenar_tabla():
    vaciar_tabla()
    sql= "select * from sistema" #cambia sistema por tu tabla
    db.cursor.execute(sql)
    filas=db.cursor.fetchall()
    for fila in filas:
        turno=fila[0]
        tvPedidos.insert("", "end",turno, text=turno, value= fila)

def eliminar():
    turno = tvPedidos.selection()[0]
    if int(turno)>0:
        sql="delete from sistema where turno="+turno #cambia sistema por tu tabla
        db.cursor.execute(sql)
        db.connection.commit()
        tvPedidos.delete(turno)
        lblMensaje.config(text="Se ha eliminado el registro correctamente.")
    else:
        lblMensaje.config(text="Seleccione un registro para eliminar.")

def nuevo():
    if modificar==False:  
        if validar():
            val=nombre.get(),apellido.get(),telefono.get()
            sql="insert into sistema (nombre,apellido,telefono) values (%s,%s,%s)"  #cambia sistema por tu tabla
            db.cursor.execute(sql,val)
            db.connection.commit()
            lblMensaje.config(text="Se ha generado un nuevo turno.", fg="green")
            llenar_tabla()
            limpiar()
        else:lblMensaje.config(text="los campos no deben estar vacios", fg="red")
    else:
        modificarFalse()

def actualizar():           # Esta funcion toca arreglarla
    if modificar==True:
        if validar():
            turno=tvPedidos.selection()[0]
            val=nombre.get(),apellido.get(),telefono.get()
            sql= "Update sistema set (nombre,apellido,telefono) values (%s,%s,%s) where turno="+turno   #cambia sistema por tu tabla
            db.cursor.execute(sql,val)
            db.connection.commit()
            lblMensaje.config(text="Se ha actualizado el pedido correctamente.", fg="green")
            llenar_tabla()
            limpiar()
        else:lblMensaje.config(text="los campos no deben estar vacios", fg="red")
    else:
        modificarTrue()

def whatsapp():
    ext = "+57"
    numero= tvPedidos.get_children[4]  #Aqui tambien toca arreglar para que reciba el numero del turno en forma
    mensaje = "Tu pedido esta listo"
    try:
        pywhatkit.sendwhatmsg_instantly(ext + numero, mensaje,)
        print("Mensaje Enviado")
    except:
        print("Ocurrio Un Error")


#Marco Ventana Principal
marco= LabelFrame(ventana, text="Formulario de Gestion de Pedidos")
marco.place(x=50, y=50, width=500,height=400)

#Labels y Entry
lblTurno= Label(marco,text="Turno").grid(column=0,row=0,padx=5,pady=5)#Label Turno
txtTurno= Entry(marco,textvariable=turno)#Entrada Turno
#txtTurno.grid(column=1,row=0)#Posicion Turno

lblNombre= Label(marco,text="Nombre").grid(column=0,row=1,padx=5,pady=5)#Label Nombre
txtNombre= Entry(marco,textvariable=nombre)#Entrada Nombre
txtNombre.grid(column=1,row=1)#Posicion Nombre

lblApellido= Label(marco,text="Apellido").grid(column=2,row=0,padx=5,pady=5)#Label Apellido
txtApellido= Entry(marco,textvariable=apellido)#Entrada Apellido
txtApellido.grid(column=3,row=0)#Posicion Apellido

lblTelefono= Label(marco,text="Telefono").grid(column=2,row=1,padx=5,pady=5)#Label Telefono
txtTelefono= Entry(marco,textvariable=telefono)#Entrada Telefono
txtTelefono.grid(column=3,row=1)#Posicion Telefono

lblMensaje=Label(marco,text="Escribe aqui tu Mensaje:", fg="red")
lblMensaje.grid(column=0,row=2,columnspan=4)

#tabla de la lista de pedidos(turnos)
tvPedidos= ttk.Treeview(marco)
tvPedidos.grid(column=0,row=3,columnspan=4)
tvPedidos["columns"]=("Turno","Nombre","Apellido","Telefono")
tvPedidos.column("#0",width=0, stretch="no")
tvPedidos.column("Turno",width=55, anchor="center")
tvPedidos.column("Nombre",width=54, anchor="center")
tvPedidos.column("Apellido",width=55, anchor="center")
tvPedidos.column("Telefono",width=70, anchor="center")
#Nombres Encabezados Tabla
tvPedidos.heading("#0",text="")
tvPedidos.heading("Turno",text="Turno",anchor="center")
tvPedidos.heading("Nombre",text="Nombre",anchor="center")
tvPedidos.heading("Apellido",text="Apellido",anchor="center")
tvPedidos.heading("Telefono",text="Telefono",anchor="center")
#Llamar evento
tvPedidos.bind("<<TreeViewSelect>>",seleccionar)

#Botones de Accion
btnEliminar= Button(marco,text="Eliminar", command=lambda:eliminar())
btnEliminar.grid(column=1,row=4)

btnNuevo= Button(marco,text="Guardar", command= lambda:nuevo())
btnNuevo.grid(column=2,row=4)

btnModificar= Button(marco,text="Seleccionar", command= lambda:actualizar())
btnModificar.grid(column=3,row=4)

btnEnviarWhatsapp= Button(marco,text="Enviar Whatsapp", command= lambda:whatsapp())
btnEnviarWhatsapp.grid(column=4,row=4)

#Funciones Botones

llenar_tabla()
ventana.mainloop()