import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox


class Clientes(tk.Frame):
    
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.cargar_registros()
        
    def widgets(self):
        self.labelframe = tk.LabelFrame(self, text="Clientes", font="sans 20 bold", bg="#C6D9E3")
        self.labelframe.place(x=20, y=20, width=250,  height=560)

        lblnombre = tk.Label(self.labelframe, text="Nombre:", font="sans 14 bold", bg="#C6D9E3")
        lblnombre.place(x=10, y=20)
        self.nombre =  ttk.Entry(self.labelframe,  font="sans 14 bold" )
        self.nombre.place(x=10, y=50, width=220, height=40)

        lblcedula = tk.Label(self.labelframe, text="Cedula:", font="sans 14 bold", bg="#C6D9E3")
        lblcedula.place(x=10,y=100)
        self.cedula =  ttk.Entry(self.labelframe,  font="sans 14 bold" )
        self.cedula.place(x=10, y=130, width=220, height=40)

        lblcelular = tk.Label(self.labelframe, text="Celular:", font="sans 14 bold", bg="#C6D9E3")
        lblcelular.place(x=10,y=180)
        self.celular =  ttk.Entry(self.labelframe,  font="sans 14 bold" )
        self.celular.place(x=10, y=210, width=220, height=40 )

        lbldireccion = tk.Label(self.labelframe, text="Direccion:",font="sans 14 bold",bg="#C6D9E3")
        lbldireccion.place(x=10,y=260)
        self.direccion =  ttk.Entry(self.labelframe,  font="sans 14 bold" )
        self.direccion.place(x=10, y=290, width=220, height=40 )

        lblcorreo = tk.Label(self.labelframe, text="Correo:", font="sans 14 bold", bg="#C6D9E3")
        lblcorreo.place(x=10,y=340)
        self.correo =  ttk.Entry(self.labelframe,  font="sans 14 bold" )
        self.correo.place(x=10, y=370, width=220, height=40 )

        bt1 = Button(self.labelframe, fg= "Black", text="Ingresar", font="sans 16 bold")
        bt1.place(x=10, y=420, width=220, height=40)

        bt2 = Button(self.labelframe, fg= "Black", text="Modificar", font="sans 16 bold")
        bt2.place(x=10, y=470, width=220, height=40)

        treFrame = Frame(self, bg="white")
        treFrame.place(x=280, y=20, width=800, height=560)

        Scrollbar_y = ttk.Scrollbar(treFrame)
        Scrollbar_y.pack(side = RIGHT, fill = Y)

        Scrollbar_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        Scrollbar_x.pack(side = BOTTOM, fill = X)

        self.tree = ttk.Treeview(treFrame, yscrollcommand = Scrollbar_y.set, xscrollcommand=Scrollbar_x.set, height=40, columns=("ID", "Nombre", "Cedula", "Celular", "Direccion", "Correo"), show="headings")

        self.tree.pack(expand=True, fill=BOTH)

        Scrollbar_y.config(command=self.tree.yview)
        Scrollbar_x.config(command=self.tree.xview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cedula", text="Cedula")
        self.tree.heading("Celular", text="Celular")
        self.tree.heading("Direccion", text="Direccion")
        self.tree.heading("Correo", text="Correo")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=150, anchor="center")
        self.tree.column("Cedula", width=120, anchor="center")
        self.tree.column("Celular", width=120, anchor="center")
        self.tree.column("Direccion", width=200, anchor="center")
        self.tree.column("Correo", width=200, anchor="center")

#--------------------------------------------------------------------------------- 

    def validar_campos(self):
        if not self.nombre or not self.cedula.get() or not self.celular.get() or not self.direccion.get() or not self.correo.get():
            messagebox.showerror("Error", "Todos los campos son requeridos. ")
            return False
        return True


#--------------------------------------------------------------------------------- 

    def registrar(self):
        if not self.validar_campos():
            return
        
        nombre = self.nombre.get()
        cedula = self.cedula.get()
        celular = self.celular.get()
        direccion = self.direccion.get()
        correo = self.correo.get()

        try:
             conn = sqlite3.connect('database.db')
             cursor = conn.cursor()
             cursor.execute("INSERT INTO clientes (nombre, cedula, celular, direccion, correo) VALUES (?,?,?,?,?)", 
                            (nombre, cedula, celular, direccion, correo))
             conn.commit()
             conn.close()
             messagebox.showinfo("Exito", "Cliente registrado correctamente")

        except sqlite3.Error as e :
            messagebox.showerror("Error", f"No se puedo registar el cliente: {e}")

#--------------------------------------------------------------------------------- 

    def  cargar_registros(self):

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes ")
            rows = cursor.fetchall()
            for row in rows :
                self.tree.insert("", "end", values = row) 
            conn.close()
        except sqlite3.Error as e:
             messagebox.showerror("Error", f"No se puedo cargar los registros: {e}")






